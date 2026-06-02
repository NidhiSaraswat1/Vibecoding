"""Unit tests for PostgreSQL report persistence."""

from contextlib import nullcontext
from datetime import UTC, datetime
from unittest.mock import Mock
from uuid import UUID

from psycopg.types.json import Jsonb

from research_agent.db.repository import PostgresReportRepository
from tests.fixtures import VALID_REPORT

REPORT_ID = UUID("550e8400-e29b-41d4-a716-446655440000")
ROW = {
    "id": REPORT_ID,
    "product_idea": VALID_REPORT.product_idea,
    "report": VALID_REPORT.model_dump(mode="json"),
    "model": "gpt-5.5",
    "created_at": datetime(2026, 5, 31, tzinfo=UTC),
}


def build_repository(row: dict[str, object] | None) -> tuple[PostgresReportRepository, Mock]:
    cursor = Mock()
    cursor.fetchone.return_value = row
    cursor_context = Mock()
    cursor_context.__enter__ = Mock(return_value=cursor)
    cursor_context.__exit__ = Mock(return_value=False)
    connection = Mock()
    connection.cursor.return_value = cursor_context
    return PostgresReportRepository(lambda: nullcontext(connection)), cursor


def test_stores_reports_as_jsonb_with_parameterized_sql() -> None:
    repository, cursor = build_repository(ROW)

    stored = repository.save(VALID_REPORT, "gpt-5.5")

    assert stored.product_idea == VALID_REPORT.product_idea
    parameters = cursor.execute.call_args.args[1]
    assert parameters[0] == VALID_REPORT.product_idea
    assert isinstance(parameters[1], Jsonb)
    assert parameters[2] == "gpt-5.5"


def test_returns_none_when_report_does_not_exist() -> None:
    repository, _ = build_repository(None)

    assert repository.find_by_id(REPORT_ID) is None
