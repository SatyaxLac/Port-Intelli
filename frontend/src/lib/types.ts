export interface Stock {
  symbol: string;
  quantity?: number;
  avg_price?: number;
  current_price?: number;
  invested: number;
  current_value: number;
  gain?: number;
  gain_loss?: number;
  gain_loss_percentage?: number;
  insight: string;
}

export interface PortfolioData {
  total_invested: number;
  total_current: number;
  net_gain: number;
  stocks: Stock[];
}

export interface AskApiResponse {
  answer?: string;
  response?: string;
}

export interface ChatMessage {
  id: string;
  type: "user" | "assistant";
  content: string;
  timestamp: Date;
}
