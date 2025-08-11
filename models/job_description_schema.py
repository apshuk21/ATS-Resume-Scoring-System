from pydantic import BaseModel, Field
from typing import List


class JobDescriptionSchema(BaseModel):
    job_title: str = Field(..., description="Title of the job role")
    location: str = Field(..., description="Job location")
    employment_type: str = Field(
        ..., description="Type of employment, e.g., Full-Time, Contract"
    )
    required_experience_years: int = Field(
        ..., description="Minimum years of experience required"
    )
    required_skills: List[str] = Field(..., description="Must-have skills for the role")
    preferred_skills: List[str] = Field(
        default_factory=list, description="Nice-to-have skills"
    )
    education_level: str = Field(..., description="Minimum education qualification")
    responsibilities: List[str] = Field(
        ..., description="Key responsibilities of the role"
    )
    benefits: List[str] = Field(
        default_factory=list, description="Perks and benefits offered"
    )
    raw_text: str = Field(..., description="Original job description text")
