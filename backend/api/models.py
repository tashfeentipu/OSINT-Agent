from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    threat_type: str = "unknown"
    entities: List[str] = Field(default_factory=list)
    risk_indicators: List[str] = Field(default_factory=list)
    confidence_score: float = 0.0
    transparency_note: str = ""


class RiskResult(BaseModel):
    risk_level: str = "Low"
    confidence_score: float = 0.0


class ReportResult(BaseModel):
    summary: str = ""
    recommended_action: str = ""


class ThreatItem(BaseModel):
    source: str
    text: str
    analysis: AnalysisResult
    risk: RiskResult
    report: ReportResult


class ThreatResponse(BaseModel):
    generated_at: datetime
    total_items: int
    results: List[ThreatItem]
