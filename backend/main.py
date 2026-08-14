import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.agents.reasoner import analyze_portfolio_data
from backend.agents.askgpt import answer_query

load_dotenv()

DEFAULT_CORS_ORIGINS = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "http://127.0.0.1:4173",
    "http://localhost:4173",
]


def _get_cors_origins() -> list[str]:
    configured_origins = os.getenv("CORS_ALLOW_ORIGINS")
    if not configured_origins:
        return DEFAULT_CORS_ORIGINS

    origins = [origin.strip() for origin in configured_origins.split(",") if origin.strip()]
    return origins or DEFAULT_CORS_ORIGINS


app = FastAPI(
    title="Port-Intelli API",
    description="AI-powered portfolio intelligence API",
    version="1.0.0"
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_cors_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str

@app.get("/portfolio")
async def get_portfolio():
    """Retrieve real-time portfolio analysis and AI insights."""
    return await run_in_threadpool(analyze_portfolio_data)

@app.post("/ask")
async def ask_portfolio_question(request: AskRequest):
    """Answer natural language queries regarding portfolio stocks."""
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty.")

    response = await run_in_threadpool(answer_query, question)
    return {"response": response}
