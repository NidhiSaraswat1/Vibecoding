"""Apply SQL migrations in filename order."""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


def main() -> int:
    load_dotenv()
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required.")

    migrations_directory = Path(__file__).resolve().parent / "migrations"
    with psycopg.connect(database_url) as connection:
        for migration_path in sorted(migrations_directory.glob("*.sql")):
            connection.execute(migration_path.read_text())
            print(f"Applied migration {migration_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
