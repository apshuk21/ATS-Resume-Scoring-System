import uuid
from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()


class ResumeSession(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hash = Column(String, unique=True, index=True)
    resume = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    outputs = relationship("AgentOutput", back_populates="session")


class AgentOutput(Base):
    __tablename__ = "agent_outputs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    agent_name = Column(String, nullable=False)
    output = Column(JSONB, nullable=False)
    hash = Column(String, nullable=False, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    session = relationship("ResumeSession", back_populates="outputs")
