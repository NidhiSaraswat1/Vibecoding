# Research Agent

A standalone Python and LangChain research agent for competitor research, market research, feature analysis, pain-point discovery, and opportunity discovery. Given an input such as `Build an AI Fitness App`, it uses OpenAI models to gather current web evidence, produces a validated JSON research report, and stores that report in PostgreSQL.

## Report contents

- competitors
- key features
- weaknesses
- customer complaints
- market opportunities
- recommended features
- supporting sources

## Requirements

- Python 3.11+
- PostgreSQL 14+
- an OpenAI API key

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
research-agent-migrate
```

Set `OPENAI_API_KEY` and `DATABASE_URL` in `.env`. The defaults use `gpt-5.5` for current web research and structured synthesis. Override `RESEARCH_MODEL` and `SYNTHESIS_MODEL` when you need a different cost, latency, or capability profile.

## Run

```bash
research-agent "Build an AI Fitness App"
```

The CLI prints the stored report ID and complete JSON report. Reports are saved in the `research_reports` table.

## Validate

```bash
pytest
ruff check .
mypy
```

## Structure

- `research_agent/agent.py`: LangChain orchestration and injectable model extension points
- `research_agent/prompts/`: research and synthesis prompts
- `research_agent/schemas/`: Pydantic schemas for structured JSON output
- `research_agent/db/`: PostgreSQL repository
- `research_agent/migrations/`: packaged PostgreSQL schema
- `tests/`: mocked unit tests; no API key or live database required
- `docs/architecture.md`: design and future-expansion notes
