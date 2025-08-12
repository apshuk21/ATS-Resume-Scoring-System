from pydantic import BaseModel, Field
from typing import List


class ImprovementSuggestion(BaseModel):
    section: str = Field(
        ..., description="Resume section to improve (e.g., Skills, Experience)"
    )
    suggestion: str = Field(..., description="Detailed improvement suggestion")
    priority: str = Field(..., description="Priority level: High, Medium, Low")


class ImprovementReport(BaseModel):
    suggestions: List[ImprovementSuggestion] = Field(
        ..., description="List of improvement suggestions"
    )
    keywords_to_add: List[str] = Field(
        default_factory=list, description="Missing keywords to include"
    )
    formatting_issues: List[str] = Field(
        default_factory=list, description="Formatting issues to fix"
    )
    overall_commentary: str = Field(
        ..., description="General advice on resume improvement"
    )
