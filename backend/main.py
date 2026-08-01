from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.agents.reasoner import analyze_portfolio_data
from backend.agents.askgpt import answer_query

load_dotenv()

app = FastAPI(
    title="Port-Intelli API",
    description="AI-powered portfolio intelligence API",
    version="1.0.0"
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
    response = await run_in_threadpool(answer_query, request.question)
    return {"response": response}
