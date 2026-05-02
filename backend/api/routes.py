from fastapi import APIRouter, Query

from api.models import ThreatResponse
from services.orchestrator import ThreatOrchestrator

router = APIRouter(tags=["threats"])

DEFAULT_FEEDS = [
    "https://thehackernews.com/feeds/posts/default?alt=rss",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
]


@router.get("/threats", response_model=ThreatResponse)
def get_threats(limit: int = Query(default=3, ge=1, le=50)) -> ThreatResponse:
    orchestrator = ThreatOrchestrator()
    return orchestrator.run(feeds=DEFAULT_FEEDS, limit=limit)
