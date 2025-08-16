import fitz
import io
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from autogen_agentchat.messages import StructuredMessage
from docx import Document
from fastapi import FastAPI, Form, File, UploadFile, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated

from models.visualization_payload_schema import AnalysisResponse
from models.session_outputs import SessionOutputsResponse, AgentOutputResponse
from pathlib import Path

from teams.ats_team import ATSTeam
from models.visualization_payload_schema import VisualizationPayloadSchema
from models.db_models import (
    Base,
    ResumeSession,
    AgentOutput as AgentOutputModel,
)
from db import check_db_connection, engine, get_table_names, get_db
from contextlib import asynccontextmanager

from sqlalchemy.orm import Session
from utils.hash_utility import compute_hash
from typing import Optional

load_dotenv()


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


def safe_model_dump(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    else:
        return str(obj)


# NEW FUNCTION: Session lookup or creation
def get_or_create_session(db: Session, resume: str, jd: str) -> ResumeSession:
    session_hash = compute_hash(resume + jd)
    existing = db.query(ResumeSession).filter_by(hash=session_hash).first()
    if existing:
        return existing
    new_session = ResumeSession(hash=session_hash, resume=resume, job_description=jd)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


# NEW FUNCTION: Cache check
def get_cached_outputs(db: Session, session_id: int) -> list[AgentOutputModel]:
    return db.query(AgentOutputModel).filter_by(session_id=session_id).all()


def prepare_for_json(obj):
    if isinstance(obj, dict):
        return {k: prepare_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [prepare_for_json(v) for v in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj


# NEW FUNCTION: Store individual agent output
def store_agent_output(
    db: Session,
    session_id: int,
    agent_name: str,
    output: dict,
    created_at: datetime,
    models_usage: Optional[dict] = None,
    hash: Optional[str] = None,
):
    safe_output = prepare_for_json(output)

    if hash is None:
        hash = compute_hash(agent_name + json.dumps(safe_output, sort_keys=True))

    db_output = AgentOutputModel(
        session_id=session_id,
        agent_name=agent_name,
        output=safe_output,
        created_at=created_at,
        models_usage=models_usage,
        hash=hash,
    )
    db.add(db_output)
    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    if os.getenv("ENV") == "development":
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created (dev mode).")
    yield
    # Shutdown logic (optional)
    print("App shutting down.")


app = FastAPI(title="ATS Resume Scoring System", version="0.1", lifespan=lifespan)

BASE_DIR = Path(__file__).parent.parent

# Mount the "static" folder to be served at /static
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/health/db")
def health_check_db():
    if check_db_connection():
        return {"status": "ok", "message": "Database connection successful"}
    return {"status": "error", "message": "Failed to connect to database"}


@app.get("/tables")
def list_tables():
    tables = get_table_names()
    return {"tables": tables}


@app.get("/", response_class=HTMLResponse)
async def serve_form():
    # Will return the HTML page with the upload form and chart container
    file_path = Path("static") / "index.html"
    return FileResponse(file_path)


@app.get("/api/session_outputs", response_model=SessionOutputsResponse)
def get_session_outputs(session_id: int, db: Session = Depends(get_db)):
    outputs = db.query(AgentOutputModel).filter_by(session_id=session_id).all()
    if not outputs:
        raise HTTPException(status_code=404, detail="No outputs found for this session")

    response = SessionOutputsResponse(
        session_id=session_id,
        outputs=[
            AgentOutputResponse(
                agent_name=o.agent_name,
                output=o.output,
                created_at=o.created_at,
                models_usage=o.models_usage,
            )
            for o in outputs
        ],
    )
    return response


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: Annotated[
        UploadFile, File(..., description="Resume file (PDF, DOCX, etc.)")
    ],
    job_description: Annotated[str, Form(..., description="Job description text")],
    db: Session = Depends(get_db),
):
    # 1. Extract text from resume
    resume_bytes = await resume.read()
    resume_text = extract_resume_text(resume.filename, resume_bytes)
    print("****Resume text****")
    print(resume_text)

    # 2. Session lookup or creation
    session = get_or_create_session(db, resume_text, job_description)
    print("##session hash", session.hash)
    print("##session id", session.id)

    # 3. Check cache
    cached_outputs = get_cached_outputs(db, session.id)
    print("##cached outputs", cached_outputs)

    if cached_outputs:
        print("Returning cached outputs")

        # 3a. Look for VisualizationAgent output
        viz_output = next(
            (o for o in cached_outputs if o.agent_name == "Visualization_Agent"), None
        )

        if viz_output:
            try:
                # Validate and reconstruct AnalysisResponse
                response_data = VisualizationPayloadSchema.model_validate(
                    viz_output.output
                )
                return AnalysisResponse(**response_data.model_dump())
            except Exception as e:
                print(f"Error reconstructing AnalysisResponse from cache: {e}")
                raise HTTPException(status_code=500, detail="Cached data invalid")

        # 3b. If VisualizationAgent output not found
        raise HTTPException(
            status_code=404, detail="VisualizationAgent output not found in cache"
        )

    # 4. Run agents
    ats_team_results = await ATSTeam().run_ats_team(
        resume_text=resume_text, job_description=job_description
    )

    # 5. Store all structured outputs
    for message in ats_team_results.messages:
        if isinstance(message, StructuredMessage):
            try:
                output_dict = message.content.model_dump()
                print("##output_dict", output_dict)
                print("****" * 10)
                usage_dict = (
                    safe_model_dump(message.models_usage)
                    if message.models_usage
                    else None
                )
                print("##usage_dict", usage_dict)
                print("****" * 10)

                safe_output = prepare_for_json(output_dict)
                hash_key = compute_hash(
                    message.source + json.dumps(safe_output, sort_keys=True)
                )

                print("##hash_key", hash_key)
                print("****" * 10)

                store_agent_output(
                    db=db,
                    session_id=session.id,
                    agent_name=message.source,
                    output=safe_output,
                    created_at=message.created_at,
                    models_usage=usage_dict,
                    hash=hash_key,
                )
            except Exception as e:
                print(f"Skipping message from {message.source}: {e}")

    # 6. Final response from Visualization Agent
    last_message: StructuredMessage[VisualizationPayloadSchema] = (
        ats_team_results.messages[-1]
    )
    VisualizationPayloadSchema.model_validate(last_message.content)
    last_message_content = last_message.content.model_dump()

    final_response = AnalysisResponse(**last_message_content)
    return final_response
