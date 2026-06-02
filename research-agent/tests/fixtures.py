"""Reusable test fixtures."""

from research_agent.schemas.report import ResearchReport

VALID_REPORT_DATA = {
    "product_idea": "Build an AI Fitness App",
    "executive_summary": "AI coaching can improve fitness-app personalization and trust.",
    "competitors": [
        {
            "name": "Example Fitness",
            "website": "https://example.com/fitness",
            "description": "A representative fitness coaching app.",
            "target_audience": "People seeking guided workouts.",
            "pricing": "Freemium subscription.",
            "key_features": ["Workout plans"],
            "weaknesses": ["Limited personalization"],
            "customer_complaints": ["Plans can feel repetitive"],
        }
    ],
    "key_features": ["Personalized workout plans"],
    "weaknesses": ["Generic recommendations"],
    "customer_complaints": ["Users want more adaptive plans"],
    "market_opportunities": [
        {
            "title": "Adaptive coaching",
            "rationale": "Users benefit from plans that respond to progress.",
            "evidence": ["Competitor plans can feel repetitive"],
            "priority": "high",
        }
    ],
    "recommended_features": [
        {
            "name": "Adaptive AI plan",
            "description": "Adjust training based on completed workouts and feedback.",
            "addresses_pain_points": ["Users want more adaptive plans"],
            "priority": "must-have",
        }
    ],
    "sources": [
        {
            "title": "Example Fitness",
            "url": "https://example.com/fitness",
            "summary": "Representative competitor source.",
        }
    ],
}

VALID_REPORT = ResearchReport.model_validate(VALID_REPORT_DATA)
