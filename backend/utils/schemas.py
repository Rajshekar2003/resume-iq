from typing import Literal

from pydantic import BaseModel, Field


class AtsScoreResponse(BaseModel):
    score: int = Field(..., ge=0, le=100)
    strengths: list[str] = Field(..., min_length=3, max_length=3)
    weaknesses: list[str] = Field(..., min_length=3, max_length=3)
    ats_tips: list[str] = Field(..., min_length=3, max_length=3)


class Keyword(BaseModel):
    keyword: str = Field(..., min_length=2, max_length=60)
    category: Literal["language", "framework", "library", "database", "cloud", "tool", "methodology", "concept", "role-specific"]
    importance: Literal["critical", "important", "nice-to-have"]


class KeywordExtractionResponse(BaseModel):
    keywords: list[Keyword] = Field(..., min_length=15, max_length=20)


class JdMatchResponse(BaseModel):
    match_percentage: int = Field(..., ge=0, le=100)
    matched_keywords: list[str] = Field(..., min_length=5, max_length=20)
    missing_keywords: list[str] = Field(..., min_length=3, max_length=15)
    recommendation: str = Field(..., min_length=50, max_length=500)


class BulletImprovementResponse(BaseModel):
    original: str = Field(..., min_length=10, max_length=500)
    improved: str = Field(..., min_length=10, max_length=500)
    changes_made: list[str] = Field(..., min_length=2, max_length=4)
    strength_score: int = Field(..., ge=1, le=10)


class RetrievalQuery(BaseModel):
    role_title: str = Field(..., min_length=5, max_length=100)
    key_skills: list[str] = Field(..., min_length=3, max_length=10)
    target_seniority: Literal["junior", "mid", "senior", "staff_plus"]


class MarketInsight(BaseModel):
    insight: str = Field(..., min_length=20, max_length=300)
    evidence_count: int = Field(..., ge=1, le=10)
    user_has_this: bool


class MarketAnalysisResponse(BaseModel):
    matched_role_title: str = Field(..., min_length=5, max_length=100)
    jobs_analyzed: int = Field(..., ge=0, le=20)
    top_required_skills: list[MarketInsight] = Field(..., min_length=3, max_length=8)
    candidate_gap_summary: str = Field(..., min_length=50, max_length=600)
    similarity_floor_triggered: bool
    avg_similarity_score: float = Field(..., ge=0.0, le=1.0)
