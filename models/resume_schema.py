from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class Experience(BaseModel):
    title: str = Field(..., description="Job title held by the candidate")
    company: str = Field(..., description="Company name")
    duration_years: float = Field(..., description="Duration in years")
    description: str = Field(..., description="Brief description of responsibilities")


class Education(BaseModel):
    degree: str = Field(..., description="Degree obtained")
    field: str = Field(..., description="Field of study")
    institution: str = Field(..., description="Name of the institution")
    year: int = Field(..., description="Year of graduation")


class FormatQuality(BaseModel):
    has_bullet_points: bool = Field(
        True, description="Whether resume uses bullet points"
    )
    has_section_headings: bool = Field(
        True, description="Whether resume has clear section headings"
    )
    readability_score: float = Field(
        0.85, description="Score between 0 and 1 indicating readability"
    )


class FileMetadata(BaseModel):
    filename: str = Field(..., description="Original filename of the resume")
    filetype: str = Field(..., description="File extension, e.g., pdf or docx")
    filesize_kb: int = Field(..., description="File size in kilobytes")


class ResumeSchema(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    email: EmailStr = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")
    summary: str = Field(..., description="Professional summary or objective")
    skills: List[str] = Field(..., description="List of technical and soft skills")
    experience: List[Experience] = Field(..., description="Work experience entries")
    education: List[Education] = Field(..., description="Educational background")
    certifications: Optional[List[str]] = Field(
        default_factory=list, description="Certifications or licenses"
    )
    format_quality: FormatQuality = Field(
        ..., description="Resume formatting quality indicators"
    )
    file_metadata: FileMetadata = Field(
        ..., description="Metadata about the uploaded resume file"
    )
