"""Pydantic schemas for validated research reports."""

from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    """Reject unknown fields so stored reports keep a predictable contract."""

    model_config = ConfigDict(extra="forbid")


class ResearchSource(StrictModel):
    title: str = Field(min_length=1, description="Human-readable title for the source")
    url: AnyHttpUrl = Field(description="Source URL")
    summary: str = Field(min_length=1, description="Relevant evidence supplied by this source")


class Competitor(StrictModel):
    name: str = Field(min_length=1)
    website: AnyHttpUrl
    description: str = Field(min_length=1)
    target_audience: str = Field(min_length=1)
    pricing: str = Field(min_length=1)
    key_features: list[str] = Field(min_length=1)
    weaknesses: list[str] = Field(min_length=1)
    customer_complaints: list[str] = Field(min_length=1)


class MarketOpportunity(StrictModel):
    title: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    evidence: list[str] = Field(min_length=1)
    priority: Literal["high", "medium", "low"]


class RecommendedFeature(StrictModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    addresses_pain_points: list[str] = Field(min_length=1)
    priority: Literal["must-have", "should-have", "could-have"]


class ResearchReport(StrictModel):
    """Structured JSON report returned by the synthesis model and stored in PostgreSQL."""

    product_idea: str = Field(min_length=1)
    executive_summary: str = Field(min_length=1)
    competitors: list[Competitor] = Field(min_length=1)
    key_features: list[str] = Field(min_length=1)
    weaknesses: list[str] = Field(min_length=1)
    customer_complaints: list[str] = Field(min_length=1)
    market_opportunities: list[MarketOpportunity] = Field(min_length=1)
    recommended_features: list[RecommendedFeature] = Field(min_length=1)
    sources: list[ResearchSource] = Field(min_length=1)
