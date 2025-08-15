from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Literal, Optional
from datetime import datetime


class ChartData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["bar", "pie", "gauge", "radar"] = Field(
        ..., description="Type of chart"
    )
    title: str = Field(..., description="Chart title")
    labels: List[str] = Field(..., description="Labels for chart axes or segments")
    values: List[float] = Field(
        ..., description="Numerical values corresponding to labels"
    )
    metadata: Optional[Dict[str, str]] = Field(
        default=None, description="Optional metadata like units, colors, or notes"
    )


class VisualizationPayloadSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    charts: Dict[str, ChartData] = Field(
        ...,
        description="Dictionary of chart identifiers mapped to chart data",
        json_schema_extra={"properties": {}},  # 👈 Forces empty properties block
    )
    summary_text: str = Field(
        ..., description="Narrative summary of resume performance"
    )
    improvement_highlights: List[str] = Field(
        ..., description="Key suggestions extracted from improvement agent"
    )
    timestamp: datetime = Field(
        ..., description="Timestamp of visualization generation"
    )
