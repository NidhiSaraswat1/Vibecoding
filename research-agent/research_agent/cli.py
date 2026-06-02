"""Command-line entry point for generating research reports."""

import argparse
import json
import os
from collections.abc import Sequence

import psycopg
from dotenv import load_dotenv

from research_agent.agent import ResearchAgent
from research_agent.db.repository import PostgresReportRepository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate and store a structured product research report."
    )
    parser.add_argument(
        "product_idea", nargs="+", help='Product idea, for example: "Build an AI Fitness App"'
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    load_dotenv()
    args = build_parser().parse_args(argv)
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required.")

    repository = PostgresReportRepository(lambda: psycopg.connect(database_url))
    agent = ResearchAgent(
        repository,
        research_model_name=os.environ.get("RESEARCH_MODEL", "gpt-5.5"),
        synthesis_model_name=os.environ.get("SYNTHESIS_MODEL", "gpt-5.5"),
    )
    result = agent.run(" ".join(args.product_idea))
    print(
        json.dumps(
            {"id": str(result.stored_report.id), "report": result.report.model_dump(mode="json")},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
