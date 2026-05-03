from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

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
        return self._run_internal(feeds=feeds, limit=limit)

    def run_with_progress(
        self,
        feeds: List[str],
        limit: int = 10,
        on_progress: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> ThreatResponse:
        return self._run_internal(feeds=feeds, limit=limit, on_progress=on_progress)

    def _run_internal(
        self,
        feeds: List[str],
        limit: int = 10,
        on_progress: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> ThreatResponse:
        if on_progress:
            on_progress({"stage": "collecting", "message": "Collecting RSS intelligence sources."})

        collected = self.collector.collect(feeds=feeds, limit=limit)
        results: List[ThreatItem] = []
        total = len(collected)

        if on_progress:
            on_progress(
                {
                    "stage": "collected",
                    "message": f"Collected {total} item(s). Starting analysis pipeline.",
                    "total_items": total,
                }
            )

        for index, item in enumerate(collected, start=1):
            source = item.get("source", "unknown")
            original_text = item.get("text", "")

            if on_progress:
                on_progress(
                    {
                        "stage": "analyzing",
                        "message": f"Analyzing item {index}/{total} from {source}.",
                        "item_index": index,
                        "total_items": total,
                        "source": source,
                    }
                )

            sanitized = self.ethics.sanitize_text(original_text)
            analysis_raw = self.analyzer.analyze(
                text=sanitized["sanitized_text"],
                transparency_note=sanitized["transparency_note"],
            )

            if on_progress:
                on_progress(
                    {
                        "stage": "scoring",
                        "message": f"Calculating risk score for item {index}/{total}.",
                        "item_index": index,
                        "total_items": total,
                        "source": source,
                    }
                )

            risk_raw = self.risk_agent.assess(analysis_raw)

            if on_progress:
                on_progress(
                    {
                        "stage": "reporting",
                        "message": f"Building report for item {index}/{total}.",
                        "item_index": index,
                        "total_items": total,
                        "source": source,
                    }
                )

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

        response = ThreatResponse(
            generated_at=datetime.utcnow(),
            total_items=len(results),
            results=results,
        )

        if on_progress:
            on_progress(
                {
                    "stage": "completed",
                    "message": f"Completed analysis for {len(results)} item(s).",
                    "total_items": len(results),
                }
            )

        return response
