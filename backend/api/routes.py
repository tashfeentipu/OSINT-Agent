from fastapi import APIRouter, Query

from api.models import ThreatResponse
from services.orchestrator import ThreatOrchestrator

router = APIRouter(tags=["threats"])

DEFAULT_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.schneier.com/blog/atom.xml",
    "https://krebsonsecurity.com/feed/",
]


@router.get("/threats", response_model=ThreatResponse)
def get_threats(limit: int = Query(default=10, ge=1, le=100)) -> ThreatResponse:
    orchestrator = ThreatOrchestrator()
    return orchestrator.run(feeds=DEFAULT_FEEDS, limit=limit)
