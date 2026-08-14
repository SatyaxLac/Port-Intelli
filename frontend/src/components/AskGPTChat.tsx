import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Bot, User, MessagesSquare } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ScrollArea } from "@/components/ui/scroll-area";
import { askPortfolioQuestion } from "@/lib/api";
import type { ChatMessage } from "@/lib/types";

const createMessageId = () => {
  const randomId = globalThis.crypto?.randomUUID?.();
  return randomId ? `msg-${randomId}` : `msg-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
};

const AskGPTChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    const question = inputValue.trim();
    const userMessage: ChatMessage = {
      id: createMessageId(),
      type: "user",
      content: question,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const answer = await askPortfolioQuestion(question);

      const assistantMessage: ChatMessage = {
        id: createMessageId(),
        type: "assistant",
        content: answer,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error asking question:", error);

      const errorMessage: ChatMessage = {
        id: createMessageId(),
        type: "assistant",
        content: "Sorry, I couldn't process your question right now. Please make sure the API server is running and try again.",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);

      const isNetworkError = error instanceof TypeError;
      toast({
        title: isNetworkError ? "Connection Error" : "Request Failed",
        description: isNetworkError
          ? "Could not connect to the AI service. Please check if the API is running on port 8000."
          : error instanceof Error
            ? error.message
            : "An unexpected error occurred.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="panel-edge flex h-[680px] flex-col overflow-hidden xl:h-[calc(100vh-286px)] xl:min-h-[620px]">
      <div className="border-b border-stone-800 bg-stone-950/70 p-4">
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <div className="grid h-9 w-9 place-items-center border border-amber-300/50 bg-amber-300/10">
                <Bot className="h-4 w-4 text-amber-200" />
              </div>
              <div>
                <h2 className="text-sm font-black uppercase tracking-[0.24em] text-stone-100">
                  Ask GPT
                </h2>
                <p className="mt-1 text-xs text-stone-500">Portfolio reasoning rail</p>
              </div>
            </div>
          </div>
          <div className="border border-emerald-300/30 bg-emerald-300/10 px-2 py-1 text-[10px] font-bold uppercase tracking-[0.16em] text-emerald-200">
            Live
          </div>
        </div>
      </div>

      <ScrollArea className="flex-1 bg-stone-950/35">
        <div className="min-h-full space-y-4 p-4">
          {messages.length === 0 && (
            <div className="grid min-h-[420px] place-items-center text-center">
              <div className="max-w-xs">
                <div className="mx-auto grid h-16 w-16 place-items-center border border-stone-700 bg-stone-900">
                  <MessagesSquare className="h-7 w-7 text-cyan-300" />
                </div>
                <p className="mt-5 text-[10px] font-bold uppercase tracking-[0.28em] text-stone-500">
                  Thread idle
                </p>
                <h3 className="mt-2 text-2xl font-black text-stone-100">
                  Ready for portfolio context.
                </h3>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}
            >
              <div className={`grid max-w-[88%] gap-2 ${message.type === "user" ? "justify-items-end" : "justify-items-start"}`}>
                <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.18em] text-stone-600">
                  {message.type === "assistant" ? <Bot className="h-3 w-3" /> : <User className="h-3 w-3" />}
                  <span>{message.type === "assistant" ? "AI desk" : "You"}</span>
                  <span>{message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
                </div>

                <div
                  className={`border px-4 py-3 text-sm leading-6 shadow-[0_12px_28px_rgba(0,0,0,0.2)] ${
                    message.type === "user"
                      ? "border-cyan-300/40 bg-cyan-300 text-stone-950"
                      : "border-stone-700 bg-stone-900 text-stone-200"
                  }`}
                >
                  <p className="whitespace-pre-wrap break-words">{message.content}</p>
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="border border-stone-700 bg-stone-900 px-4 py-3">
                <div className="flex items-center gap-2">
                  <span className="h-2 w-2 animate-bounce bg-amber-300" />
                  <span className="h-2 w-2 animate-bounce bg-amber-300 [animation-delay:0.1s]" />
                  <span className="h-2 w-2 animate-bounce bg-amber-300 [animation-delay:0.2s]" />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </ScrollArea>

      <div className="border-t border-stone-800 bg-stone-950 p-3">
        <form onSubmit={handleSubmit} className="grid grid-cols-[minmax(0,1fr)_48px] gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask about a holding, news, or portfolio move"
            disabled={isLoading}
            className="h-12 rounded-none border-stone-700 bg-stone-900 px-4 text-sm text-stone-100 placeholder:text-stone-600 focus-visible:ring-cyan-300"
          />
          <Button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="h-12 rounded-none border border-cyan-300/40 bg-cyan-300 p-0 text-stone-950 hover:bg-cyan-200"
            size="icon"
            aria-label="Send question"
          >
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </div>
    </section>
  );
};

export default AskGPTChat;
