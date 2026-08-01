# Port-Intelli - Project Context & Developer Guide

Port-Intelli is a full-stack financial portfolio assistant. It combines configured holdings, live market prices, financial news, and Gemini-generated summaries into a local dashboard and chat interface.

## Architecture

- Backend: FastAPI app served from `backend/main.py`.
- Frontend: React, TypeScript, Vite, Tailwind CSS, shadcn/Radix UI, and TanStack Query.
- Holdings data: Local JSON configuration through `backend/portfolio/holdings.py`.
- Price data: yfinance through `backend/data/price_fetcher.py`.
- News data: Serper.dev through `backend/data/news_fetcher.py` and `backend/data/serper_client.py`.
- LLM summaries: Google Gemini through `backend/agents/gemini_summarizer.py`.

## Backend Modules

| File | Responsibility |
| --- | --- |
| `backend/main.py` | FastAPI app setup, CORS, `/portfolio`, and `/ask`. |
| `backend/portfolio/holdings.py` | Local holdings loading and sample fallback data. |
| `backend/agents/reasoner.py` | Orchestrates holdings, prices, news, summaries, and portfolio totals. |
| `backend/agents/askgpt.py` | Answers natural-language portfolio questions. |
| `backend/agents/gemini_summarizer.py` | Gemini prompt construction, generation, and summary cache. |
| `backend/data/price_fetcher.py` | yfinance NSE price lookup. |
| `backend/data/news_fetcher.py` | Symbol-specific news lookup and cache. |
| `backend/data/serper_client.py` | Serper.dev request and response normalization. |

## Frontend Modules

| File | Responsibility |
| --- | --- |
| `frontend/src/App.tsx` | Providers, toasts, router, and root route setup. |
| `frontend/src/pages/Index.tsx` | Main Port-Intelli dashboard shell. |
| `frontend/src/components/PortfolioOverview.tsx` | Portfolio metrics, loading/error states, and holdings list. |
| `frontend/src/components/StockCard.tsx` | Individual holding row/card. |
| `frontend/src/components/AskGPTChat.tsx` | Chat rail for portfolio questions. |
| `frontend/src/lib/api.ts` | API base URL and typed frontend fetch helpers. |
| `frontend/src/lib/types.ts` | Shared frontend API and UI types. |

## API Contracts

`GET /portfolio`

Returns:

```json
{
  "total_invested": 150000.0,
  "total_current": 165000.0,
  "net_gain": 15000.0,
  "stocks": [
    {
      "symbol": "TATAMOTORS",
      "quantity": 50,
      "avg_price": 600.0,
      "current_price": 650.0,
      "invested": 30000.0,
      "current_value": 32500.0,
      "gain": 2500.0,
      "insight": "Concise AI-generated market context."
    }
  ]
}
```

`POST /ask`

Request:

```json
{
  "question": "Why is TATAMOTORS down?"
}
```

Response:

```json
{
  "response": "..."
}
```

## Environment Variables

```env
PORTFOLIO_HOLDINGS_JSON=[{"symbol":"TATAMOTORS","quantity":50,"avg_price":620.0}]
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
```

## Running Locally

Backend:

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Attribution

This derivative project keeps the original MIT License attribution for Jaidev K in `LICENSE`.
