from datetime import datetime
from typing import Dict, List

from agents.analyzer_agent import AnalyzerAgent
from agents.collector_agent import CollectorAgent
from agents.reporter_agent import ReporterAgent
from agents.risk_agent import RiskAgent
from api.models import AnalysisResult, ReportResult, RiskResult, ThreatItem, ThreatResponse
from services.ethical_ai import EthicalAIService


class ThreatOrchestrator:
    """Runs full pipeline: collect -> analyze -> risk -> report."""

    def __init__(self) -> None:
        self.collector = CollectorAgent()
        self.analyzer = AnalyzerAgent()
        self.risk_agent = RiskAgent()
        self.reporter = ReporterAgent()
        self.ethics = EthicalAIService()

    def run(self, feeds: List[str], limit: int = 10) -> ThreatResponse:
        collected = self.collector.collect(feeds=feeds, limit=limit)
        results: List[ThreatItem] = []

        for item in collected:
            source = item.get("source", "unknown")
            original_text = item.get("text", "")

            sanitized = self.ethics.sanitize_text(original_text)
            analysis_raw = self.analyzer.analyze(
                text=sanitized["sanitized_text"],
                transparency_note=sanitized["transparency_note"],
            )
            risk_raw = self.risk_agent.assess(analysis_raw)
            report_raw = self.reporter.report(source=source, analysis=analysis_raw, risk=risk_raw)

            results.append(
                ThreatItem(
                    source=source,
                    text=sanitized["sanitized_text"],
                    analysis=AnalysisResult(**analysis_raw),
                    risk=RiskResult(**risk_raw),
                    report=ReportResult(**report_raw),
                )
            )

        return ThreatResponse(
            generated_at=datetime.utcnow(),
            total_items=len(results),
            results=results,
        )
