from pydantic import BaseModel, Field
from typing import List


class SkillsMatch(BaseModel):
    score: int = Field(..., description="Score for skill match")
    max_score: int = Field(..., description="Maximum possible score for skills")
    matched_skills: List[str] = Field(
        ..., description="Skills found in both resume and JD"
    )
    missing_skills: List[str] = Field(
        default_factory=list, description="Skills required but missing in resume"
    )


class ExperienceRelevance(BaseModel):
    score: int = Field(..., description="Score for experience relevance")
    max_score: int = Field(..., description="Maximum possible score for experience")
    matched_years: float = Field(..., description="Years of experience in resume")
    required_years: float = Field(..., description="Years of experience required by JD")


class EducationAlignment(BaseModel):
    score: int = Field(..., description="Score for education match")
    max_score: int = Field(..., description="Maximum possible score for education")
    match: bool = Field(..., description="Whether education level matches JD")


class FormatAndStructure(BaseModel):
    score: int = Field(..., description="Score for resume formatting")
    max_score: int = Field(..., description="Maximum possible score for formatting")
    issues: List[str] = Field(
        default_factory=list, description="Formatting issues found"
    )


class KeywordOptimization(BaseModel):
    score: int = Field(..., description="Score for keyword optimization")
    max_score: int = Field(..., description="Maximum possible score for keywords")
    missing_keywords: List[str] = Field(
        default_factory=list, description="Important keywords missing from resume"
    )


class BenchmarkComparison(BaseModel):
    percentile: int = Field(..., description="Percentile compared to other applicants")
    industry_average_score: int = Field(
        ..., description="Average score across similar roles"
    )


class ScoreBreakdown(BaseModel):
    skills_match: SkillsMatch
    experience_relevance: ExperienceRelevance
    education_alignment: EducationAlignment
    format_and_structure: FormatAndStructure
    keyword_optimization: KeywordOptimization


class ScoreReportSchema(BaseModel):
    total_score: int = Field(..., description="Final score assigned to resume")
    confidence: float = Field(..., description="Confidence level of scoring")
    score_breakdown: ScoreBreakdown = Field(
        ..., description="Detailed breakdown of scoring components"
    )
    benchmark_comparison: BenchmarkComparison = Field(
        ..., description="Comparison with industry benchmarks"
    )
    timestamp: str = Field(..., description="Timestamp of scoring event in ISO format")
