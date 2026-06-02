"""Structured-report synthesis prompt."""

SYNTHESIS_SYSTEM_PROMPT = """You are a senior product strategist. Convert the supplied research
dossier into a structured research report.

Rules:
- satisfy every field in the requested schema
- preserve source URLs and use only URLs grounded in the dossier
- include direct competitors and useful adjacent competitors
- aggregate cross-market key features, weaknesses, and complaints
- make opportunities evidence-driven
- make recommended features actionable and map them to pain points
- do not invent facts; clearly express uncertainty in the relevant text field
  when evidence is limited
"""


def build_synthesis_prompt(product_idea: str, dossier: str) -> str:
    return f"""Product idea: {product_idea!r}

Research dossier:
{dossier}"""
