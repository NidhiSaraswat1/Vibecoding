"""PostgreSQL persistence for research reports."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol
from uuid import UUID

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from research_agent.schemas.report import ResearchReport


@dataclass(frozen=True)
class StoredResearchReport:
    id: UUID
    product_idea: str
    report: ResearchReport
    model: str
    created_at: datetime


class ReportRepository(Protocol):
    def save(self, report: ResearchReport, model: str) -> StoredResearchReport: ...

    def find_by_id(self, report_id: UUID) -> StoredResearchReport | None: ...


class PostgresReportRepository:
    """Store validated reports as JSONB using short-lived database connections."""

    def __init__(self, connect: Callable[[], Connection[Any]]) -> None:
        self._connect = connect

    def save(self, report: ResearchReport, model: str) -> StoredResearchReport:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """INSERT INTO research_reports (product_idea, report, model)
                   VALUES (%s, %s, %s)
                   RETURNING id, product_idea, report, model, created_at""",
                (report.product_idea, Jsonb(report.model_dump(mode="json")), model),
            )
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError("PostgreSQL did not return the inserted research report.")
            return _map_row(row)

    def find_by_id(self, report_id: UUID) -> StoredResearchReport | None:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """SELECT id, product_idea, report, model, created_at
                   FROM research_reports
                   WHERE id = %s""",
                (report_id,),
            )
            row = cursor.fetchone()
            return _map_row(row) if row is not None else None


def _map_row(row: dict[str, Any]) -> StoredResearchReport:
    return StoredResearchReport(
        id=row["id"],
        product_idea=row["product_idea"],
        report=ResearchReport.model_validate(row["report"]),
        model=row["model"],
        created_at=row["created_at"],
    )
