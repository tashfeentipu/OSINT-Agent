from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router as threat_router


app = FastAPI(title="AI Threat Intelligence API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(threat_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
