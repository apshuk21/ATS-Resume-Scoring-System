import fitz
import io
from autogen_agentchat.messages import StructuredMessage
from docx import Document
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated

from models.visualization_payload_schema import AnalysisResponse
from pathlib import Path

# from datetime import datetime, timezone
from teams.ats_team import ATSTeam
from models.visualization_payload_schema import VisualizationPayloadSchema


def extract_resume_text(filename: str, file_bytes: bytes) -> str:
    if filename.lower().endswith(".pdf"):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        try:
            return "\n".join(page.get_text() for page in doc)
        finally:
            doc.close()
    elif filename.lower().endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX.")


app = FastAPI(title="ATS Resume Scoring System", version="0.1")

BASE_DIR = Path(__file__).parent.parent

# Mount the "static" folder to be served at /static
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_form():
    # Will return the HTML page with the upload form and chart container
    file_path = Path("static") / "index.html"
    return FileResponse(file_path)


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: Annotated[
        UploadFile, File(..., description="Resume file (PDF, DOCX, etc.)")
    ],
    job_description: Annotated[str, Form(..., description="Job description text")],
):
    # 1. Extract text from resume
    resume_bytes = await resume.read()
    resume_text = extract_resume_text(resume.filename, resume_bytes)
    print("****Resume text****")
    print(resume_text)

    ats_team_results = await ATSTeam().run_ats_team(
        resume_text=resume_text, job_description=job_description
    )

    last_message: StructuredMessage[VisualizationPayloadSchema] = (
        ats_team_results.messages[-1]
    )
    print(f"##last_message: {last_message}\n")
    print("***" * 20)
    VisualizationPayloadSchema.model_validate(last_message.content)
    last_message_content = last_message.content.model_dump()
    print(f"##last_message_content: {last_message_content}\n")

    final_response = AnalysisResponse(**last_message_content)

    # # === Step 2: Return dummy response ===
    # dummy_response = AnalysisResponse(
    #     charts={
    #         "skill_match": ChartData(
    #             type="bar",
    #             title="Skill Match Overview",
    #             labels=["React", "TypeScript", "GraphQL", "Cypress"],
    #             values=[0.95, 0.9, 0.7, 0.4],
    #             metadata={"unit": "match_score", "color": "blue"},
    #         ),
    #         "coverage_gauge": ChartData(
    #             type="gauge",
    #             title="Resume Coverage Score",
    #             labels=["Coverage"],
    #             values=[78.5],
    #             metadata={"unit": "%", "color": "green"},
    #         ),
    #     },
    #     summary_text="The resume demonstrates strong alignment with frontend skills, especially React and TypeScript. Coverage of testing and GraphQL is moderate.",
    #     improvement_highlights=[
    #         "Add Cypress testing experience",
    #         "Include accessibility implementation details",
    #         "Mention experience with design systems",
    #     ],
    #     timestamp=datetime.now(timezone.utc),
    # )
    return final_response
