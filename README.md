# Port-Intelli

Port-Intelli is a personal AI-powered portfolio intelligence dashboard for tracking holdings, live NSE prices, recent market news, and AI-generated stock context from one local app.

The app combines a FastAPI backend with a React and Tailwind frontend. The backend loads holdings from local configuration or sample development data, enriches them with yfinance prices and Serper news, and uses Gemini to summarize what may be moving each stock. The frontend presents the portfolio in a trading-console style interface with an Ask GPT panel for natural-language questions about the portfolio.

## Features

- Local holdings input with sample fallback data for development.
- Live NSE price enrichment through yfinance.
- Recent stock news lookup through Serper.dev.
- Gemini summaries for concise stock-level market context.
- Portfolio totals for invested value, current value, net return, strongest holding, and weakest holding.
- Chat-style portfolio assistant using the same backend context.
- Local-first setup using environment variables for API credentials.

## Tech Stack

- Backend: Python, FastAPI, yfinance, Serper.dev, Google Gemini.
- Frontend: React, TypeScript, Vite, Tailwind CSS, shadcn/Radix UI, TanStack Query.

## Project Structure

```text
backend/
  main.py                 FastAPI app and API routes
  agents/
    askgpt.py             Portfolio question answering
    gemini_summarizer.py  Gemini summarization helper
    reasoner.py           Portfolio enrichment and aggregation
  data/
    news_fetcher.py       Symbol news cache and lookup
    price_fetcher.py      yfinance price lookup
    serper_client.py      Serper news API client
  portfolio/
    holdings.py           Local holdings provider

frontend/
  src/
    pages/Index.tsx       Main dashboard shell
    components/           Portfolio and chat UI
    lib/                  API helpers and shared types
```

## Environment Variables

Create a `.env` file in the project root:

```env
PORTFOLIO_HOLDINGS_JSON=[{"symbol":"TATAMOTORS","quantity":50,"avg_price":620.0}]
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
CORS_ALLOW_ORIGINS=http://127.0.0.1:8080,http://localhost:8080
```

If `PORTFOLIO_HOLDINGS_JSON` is not set, the backend falls back to sample holdings for development.
If `CORS_ALLOW_ORIGINS` is not set, the API allows the local Vite dev and preview origins.

## Run Locally

Install Python dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn backend.main:app --reload --port 8000
```

Install and start the frontend:

```bash
cd frontend
npm install
npm run dev
```

The frontend defaults to `http://127.0.0.1:8080` and calls the backend at `http://127.0.0.1:8000`.

## API

`GET /portfolio`

Returns total invested value, current value, net gain, and enriched stock rows.

`POST /ask`

Accepts:

```json
{
  "question": "Why is TATAMOTORS down?"
}
```

Returns:

```json
{
  "response": "..."
}
```

## Tests And Checks

Backend tests:

```bash
.venv\Scripts\python.exe -m unittest discover -s . -p "test*.py"
```

Frontend checks:

```bash
cd frontend
npm run lint
npm run build
```

