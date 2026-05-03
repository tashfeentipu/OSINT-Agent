import json
import threading
from queue import Empty, Queue
from typing import Any, Dict, Generator, Optional

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

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


def _sse_event(event: str, payload: Dict[str, Any]) -> str:
    return f"event: {event}\ndata: {json.dumps(payload)}\n\n"


@router.get("/threats/stream")
def stream_threats(limit: int = Query(default=12, ge=1, le=50)) -> StreamingResponse:
    def event_stream() -> Generator[str, None, None]:
        orchestrator = ThreatOrchestrator()
        progress_queue: Queue[Dict[str, Any]] = Queue()
        result_holder: Dict[str, Optional[ThreatResponse]] = {"response": None}
        error_holder: Dict[str, Optional[str]] = {"error": None}
        done = threading.Event()

        def on_progress(payload: Dict[str, Any]) -> None:
            progress_queue.put(payload)

        def run_pipeline() -> None:
            try:
                result_holder["response"] = orchestrator.run_with_progress(
                    feeds=DEFAULT_FEEDS,
                    limit=limit,
                    on_progress=on_progress,
                )
            except Exception as exc:
                error_holder["error"] = str(exc)
            finally:
                done.set()

        yield _sse_event("progress", {"stage": "starting", "message": "Threat analysis request started."})

        worker = threading.Thread(target=run_pipeline, daemon=True)
        worker.start()

        while not done.is_set() or not progress_queue.empty():
            try:
                payload = progress_queue.get(timeout=0.2)
            except Empty:
                continue
            yield _sse_event("progress", payload)

        if error_holder["error"]:
            yield _sse_event("error", {"message": error_holder["error"]})
            yield _sse_event("done", {"message": "Stream completed with error."})
            return

        response = result_holder["response"]
        if response is None:
            yield _sse_event("error", {"message": "No result produced by orchestrator."})
            yield _sse_event("done", {"message": "Stream completed with error."})
            return

        yield _sse_event("result", response.model_dump(mode="json"))
        yield _sse_event("done", {"message": "Stream completed."})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
