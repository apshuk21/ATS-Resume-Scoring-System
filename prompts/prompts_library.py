from enum import Enum


class SystemPrompts(str, Enum):
    RESUME_PROCESSING_AGENT = "Extract key skills, experience, education, certifications, and formatting quality from the resume provided in the `resume` field of the input."
    JOB_DESCRIPTION_AGENT = "Analyze the job description in the `job_description` field and extract required skills, preferred skills, responsibilities, and qualifications."
    SCORING_AGENT = "Compare the structured resume and job description inputs. Generate a detailed score breakdown based on skills match, experience relevance, education alignment, formatting quality, and keyword optimization."
    IMPROVEMENT_AGENT = "Suggest specific improvements to the resume based on the scoring breakdown. Focus on missing skills, formatting issues, and keyword gaps relevant to the job description."
    VISUALIZATION_AGENT = "Generate a structured visualization-ready output from the scoring report, including charts, matched/missing skills, and percentile comparisons."
