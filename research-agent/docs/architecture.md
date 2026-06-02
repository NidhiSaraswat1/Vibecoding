# Research Agent architecture

## Workflow

1. `ResearchAgent.run()` validates a product idea such as `Build an AI Fitness App`.
2. The evidence stage uses LangChain's `ChatOpenAI` integration with the OpenAI Responses API and its built-in `web_search_preview` tool. Its prompt requests competitor, market, feature, pain-point, and opportunity evidence with URLs.
3. The synthesis stage uses LangChain's `with_structured_output()` method and a Pydantic schema. This keeps source gathering flexible while ensuring that the final report is validated, structured JSON.
4. The validated report is saved as PostgreSQL `JSONB` with the synthesis model and creation timestamp.

## Why two model calls?

Evidence gathering and report formatting have different failure modes. Keeping them separate lets future contributors replace the research source, add MCP connectors, use proprietary datasets, or run multiple specialist researchers without changing report persistence.

## Extension points

- Implement the `ReportRepository` protocol to add another persistence layer.
- Inject alternative LangChain-compatible models for tests, tracing, retries, or provider wrappers.
- Add fields to the Pydantic schemas and SQL JSONB report without a table redesign.
- Add prompt modules for vertical-specific research workflows.
- Add a service or queue adapter around `ResearchAgent.run()` for asynchronous workloads.

## References

The implementation follows the official LangChain Python documentation for [ChatOpenAI and the Responses API](https://docs.langchain.com/oss/python/integrations/chat/openai/) and [structured model output](https://docs.langchain.com/oss/python/langchain-models#structured-output). The OpenAI model defaults follow the official [OpenAI models guide](https://developers.openai.com/api/docs/models).
