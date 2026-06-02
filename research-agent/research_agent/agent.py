"""LangChain orchestration for market and competitor research."""

from dataclasses import dataclass
from typing import Any, Protocol

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from research_agent.db.repository import ReportRepository, StoredResearchReport
from research_agent.prompts.research import RESEARCH_SYSTEM_PROMPT, build_research_prompt
from research_agent.prompts.synthesis import SYNTHESIS_SYSTEM_PROMPT, build_synthesis_prompt
from research_agent.schemas.report import ResearchReport


class Invokable(Protocol):
    def invoke(self, input: Any, **kwargs: Any) -> Any: ...


@dataclass(frozen=True)
class ResearchResult:
    report: ResearchReport
    stored_report: StoredResearchReport


class ResearchAgent:
    """Gather current evidence, synthesize structured JSON, and persist a report."""

    def __init__(
        self,
        repository: ReportRepository,
        *,
        research_model: Invokable | None = None,
        synthesis_model: Invokable | None = None,
        research_model_name: str = "gpt-5.5",
        synthesis_model_name: str = "gpt-5.5",
    ) -> None:
        self._repository = repository
        self._research_model_name = research_model_name
        self._synthesis_model_name = synthesis_model_name
        self._research_model = research_model or ChatOpenAI(
            model=research_model_name,
            use_responses_api=True,
        ).bind_tools([{"type": "web_search_preview"}])
        self._synthesis_model = synthesis_model or ChatOpenAI(
            model=synthesis_model_name,
            use_responses_api=True,
        ).with_structured_output(ResearchReport, method="json_schema")

    def run(self, product_idea: str) -> ResearchResult:
        normalized_idea = product_idea.strip()
        if not normalized_idea:
            raise ValueError("A product idea is required.")

        dossier = self._gather_evidence(normalized_idea)
        report = self._synthesize_report(normalized_idea, dossier)
        stored_report = self._repository.save(report, self._synthesis_model_name)
        return ResearchResult(report=report, stored_report=stored_report)

    def _gather_evidence(self, product_idea: str) -> str:
        response = self._research_model.invoke(
            [
                SystemMessage(content=RESEARCH_SYSTEM_PROMPT),
                HumanMessage(content=build_research_prompt(product_idea)),
            ]
        )
        dossier = _extract_text(response)
        if not dossier:
            raise RuntimeError("The research model returned an empty evidence dossier.")
        return dossier

    def _synthesize_report(self, product_idea: str, dossier: str) -> ResearchReport:
        response = self._synthesis_model.invoke(
            [
                SystemMessage(content=SYNTHESIS_SYSTEM_PROMPT),
                HumanMessage(content=build_synthesis_prompt(product_idea, dossier)),
            ]
        )
        return ResearchReport.model_validate(response)


def _extract_text(response: Any) -> str:
    """Extract text from LangChain message formats returned by chat or Responses API models."""

    content = response.content if isinstance(response, BaseMessage) else response
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        text_blocks = [
            block["text"]
            for block in content
            if isinstance(block, dict) and block.get("type") in {"text", "output_text"}
        ]
        return "\n".join(text_blocks).strip()
    if isinstance(response, AIMessage):
        return response.text.strip()
    return ""
