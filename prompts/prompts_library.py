from enum import Enum


class SystemPrompts(str, Enum):
    RESUME_PROCESSING_AGENT = "Extract key skills and experience from the resume provided in `resume` field of the input."
    JOB_DESCRIPTION_AGENT = (
        "Analyze the job description in the `job_description` field and extract required skills.",
    )
    SCORING_AGENT = ("",)
    IMPROVEMENT_AGENT = ("",)
    VISUALIZATION_AGENT = ""
