from pydantic import BaseModel, Field


class AtsScoreResponse(BaseModel):
    score: int = Field(..., ge=0, le=100)
    strengths: list[str] = Field(..., min_length=3, max_length=3)
    weaknesses: list[str] = Field(..., min_length=3, max_length=3)
    ats_tips: list[str] = Field(..., min_length=3, max_length=3)
