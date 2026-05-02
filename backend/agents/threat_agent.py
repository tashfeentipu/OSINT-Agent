from datetime import datetime
from typing import List

from api.models import ThreatItem, ThreatResponse
from services.nlp_service import NLPThreatDetectionService
from services.osint_service import OSINTIngestionService
from services.risk_service import RiskScoringService


class ThreatIntelligenceAgent:
    """Coordinates ingestion, NLP detection, and risk scoring."""

    def __init__(self) -> None:
        self.osint_service = OSINTIngestionService()
        self.nlp_service = NLPThreatDetectionService()
        self.risk_service = RiskScoringService()

    def collect_and_assess(self, feeds: List[str], limit: int = 10) -> ThreatResponse:
        raw_items = self.osint_service.ingest_from_feeds(feeds=feeds, limit=limit)

        threats: List[ThreatItem] = []
        for item in raw_items:
            detection = self.nlp_service.detect(item["text"])
            score = self.risk_service.score(
                matched_keywords=detection["matched_keywords"],
                category=detection["category"],
            )

            threats.append(
                ThreatItem(
                    title=item["title"],
                    link=item["link"],
                    summary=item["summary"],
                    source=item["source"],
                    published=item["published"],
                    matched_keywords=detection["matched_keywords"],
                    threat_category=detection["category"],
                    risk_score=score["risk_score"],
                    severity=score["severity"],
                )
            )

        threats.sort(key=lambda t: t.risk_score, reverse=True)

        return ThreatResponse(
            generated_at=datetime.utcnow(),
            total_items=len(threats),
            threats=threats,
        )
