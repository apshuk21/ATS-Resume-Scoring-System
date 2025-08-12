from pydantic import BaseModel, Field
from typing import List, Dict, Literal


class ChartData(BaseModel):
    type: Literal["bar", "pie", "gauge", "radar"] = Field(
        ..., description="Type of chart"
    )
    title: str = Field(..., description="Chart title")
    labels: List[str] = Field(..., description="Labels for chart axes or segments")
    values: List[float] = Field(
        ..., description="Numerical values corresponding to labels"
    )
    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Optional metadata like units, colors, or notes",
    )


class VisualizationPayload(BaseModel):
    charts: Dict[str, ChartData] = Field(
        ..., description="Dictionary of chart identifiers mapped to chart data"
    )
    summary_text: str = Field(
        ..., description="Narrative summary of resume performance"
    )
    improvement_highlights: List[str] = Field(
        ..., description="Key suggestions extracted from improvement agent"
    )
    timestamp: str = Field(..., description="Timestamp of visualization generation")
