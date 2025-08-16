from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Response schema
class AgentOutputResponse(BaseModel):
    agent_name: str
    output: dict
    created_at: datetime
    models_usage: Optional[dict] = None


class SessionOutputsResponse(BaseModel):
    session_id: int
    outputs: List[AgentOutputResponse]
