"""Unit tests for the LangChain research orchestration."""

from typing import Any
from unittest.mock import Mock

import pytest
from langchain_core.messages import AIMessage
from pydantic import ValidationError

from research_agent.agent import ResearchAgent
from tests.fixtures import VALID_REPORT, VALID_REPORT_DATA


class StubModel:
    def __init__(self, response: Any) -> None:
        self.response = response
        self.invocations: list[Any] = []

    def invoke(self, input: Any, **kwargs: Any) -> Any:
        self.invocations.append(input)
        return self.response


def test_gathers_evidence_creates_structured_report_and_persists_it() -> None:
    research_model = StubModel(
        AIMessage(content="Evidence dossier with https://example.com/fitness")
    )
    synthesis_model = StubModel(VALID_REPORT)
    repository = Mock()
    repository.save.return_value = Mock()
    agent = ResearchAgent(
        repository, research_model=research_model, synthesis_model=synthesis_model
    )

    result = agent.run("  Build an AI Fitness App  ")

    assert result.report == VALID_REPORT
    assert len(research_model.invocations) == 1
    assert len(synthesis_model.invocations) == 1
    repository.save.assert_called_once_with(VALID_REPORT, "gpt-5.5")


def test_rejects_blank_product_ideas_before_calling_models() -> None:
    research_model = StubModel(AIMessage(content="unused"))
    agent = ResearchAgent(
        Mock(), research_model=research_model, synthesis_model=StubModel(VALID_REPORT)
    )

    with pytest.raises(ValueError, match="A product idea is required"):
        agent.run("   ")

    assert research_model.invocations == []


def test_rejects_invalid_structured_reports() -> None:
    agent = ResearchAgent(
        Mock(),
        research_model=StubModel(AIMessage(content="Evidence")),
        synthesis_model=StubModel({"product_idea": "Incomplete"}),
    )

    with pytest.raises(ValidationError):
        agent.run("Build an AI Fitness App")


def test_extracts_responses_api_text_blocks() -> None:
    research_model = StubModel(AIMessage(content=[{"type": "output_text", "text": "Evidence"}]))
    repository = Mock()
    repository.save.return_value = Mock()
    agent = ResearchAgent(
        repository,
        research_model=research_model,
        synthesis_model=StubModel(VALID_REPORT_DATA),
    )

    assert agent.run("Build an AI Fitness App").report == VALID_REPORT
