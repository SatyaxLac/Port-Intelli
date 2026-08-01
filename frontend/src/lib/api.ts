import type { AskApiResponse, PortfolioData } from "@/lib/types";

export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const API_ENDPOINTS = {
  PORTFOLIO: `${API_BASE_URL}/portfolio`,
  ASK: `${API_BASE_URL}/ask`,
};

const parseJsonResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json() as Promise<T>;
};

export const fetchPortfolio = async (): Promise<PortfolioData> => {
  const response = await fetch(API_ENDPOINTS.PORTFOLIO);
  return parseJsonResponse<PortfolioData>(response);
};

export const askPortfolioQuestion = async (question: string): Promise<string> => {
  const response = await fetch(API_ENDPOINTS.ASK, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  const data = await parseJsonResponse<AskApiResponse>(response);
  return data.answer || data.response || "I received your question but couldn't generate a response.";
};
