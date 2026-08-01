import { useState } from "react";
import PortfolioOverview from "@/components/PortfolioOverview";
import AskGPTChat from "@/components/AskGPTChat";
import {
  Activity,
  Bot,
  CircleDollarSign,
  RefreshCw,
  Satellite,
  ShieldCheck,
  TrendingUp,
  Zap,
} from "lucide-react";

const Index = () => {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setRefreshTrigger((prev) => prev + 1);
    setTimeout(() => setIsRefreshing(false), 1000);
  };

  const statusItems = [
    { label: "Holdings", value: "Local", icon: ShieldCheck, tone: "text-emerald-300" },
    { label: "Prices", value: "NSE Live", icon: Activity, tone: "text-cyan-300" },
    { label: "Model", value: "Gemini", icon: Bot, tone: "text-amber-300" },
  ];

  return (
    <div className="terminal-shell min-h-screen text-stone-100">
      <div className="relative mx-auto max-w-[1600px] px-3 py-3 sm:px-5 lg:px-6">
        <div className="grid min-h-[calc(100vh-24px)] gap-3 lg:grid-cols-[76px_minmax(0,1fr)]">
          <aside className="hidden flex-col justify-between border border-stone-700/60 bg-stone-950/85 p-3 lg:flex">
            <div className="space-y-5">
              <div className="grid h-12 w-12 place-items-center border border-amber-300/50 bg-amber-300 text-stone-950">
                <TrendingUp className="h-6 w-6" />
              </div>

              <div className="space-y-2">
                {statusItems.map((item) => (
                  <div
                    key={item.label}
                    className="group grid h-12 w-12 place-items-center border border-stone-800 bg-stone-900/80"
                    title={`${item.label}: ${item.value}`}
                  >
                    <item.icon className={`h-4 w-4 ${item.tone}`} />
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <div className="h-12 w-12 border border-stone-800 bg-[linear-gradient(135deg,#27221a_0%,#080806_100%)]" />
              <div className="grid h-12 w-12 place-items-center border border-stone-800 bg-stone-900/80">
                <Zap className="h-4 w-4 text-amber-300" />
              </div>
            </div>
          </aside>

          <div className="flex min-w-0 flex-col gap-3">
            <header className="panel-edge overflow-hidden">
              <div className="grid gap-4 p-4 md:grid-cols-[minmax(0,1fr)_auto] md:items-center lg:p-5">
                <div className="min-w-0">
                  <div className="mb-3 flex flex-wrap items-center gap-2">
                    <span className="border border-amber-300/40 bg-amber-300/10 px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.28em] text-amber-200">
                      Port-Intelli
                    </span>
                    <span className="border border-stone-700 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.24em] text-stone-400">
                      Trading console
                    </span>
                  </div>
                  <h1 className="max-w-4xl text-3xl font-black leading-[0.95] tracking-normal text-stone-50 sm:text-5xl lg:text-6xl">
                    Port-Intelli portfolio intelligence, rebuilt for fast decisions.
                  </h1>
                </div>

                <div className="grid gap-3 sm:grid-cols-[1fr_auto] md:min-w-[420px]">
                  <div className="grid grid-cols-3 border border-stone-800 bg-stone-950/70">
                    {statusItems.map((item) => (
                      <div key={item.label} className="border-r border-stone-800 p-3 last:border-r-0">
                        <div className="flex items-center gap-2">
                          <item.icon className={`h-3.5 w-3.5 ${item.tone}`} />
                          <span className="text-[10px] font-semibold uppercase tracking-[0.18em] text-stone-500">
                            {item.label}
                          </span>
                        </div>
                        <p className="mt-2 truncate font-mono text-xs font-semibold text-stone-200">
                          {item.value}
                        </p>
                      </div>
                    ))}
                  </div>

                  <button
                    onClick={handleRefresh}
                    className="inline-flex min-h-16 items-center justify-center gap-2 border border-cyan-300/40 bg-cyan-300 px-4 text-sm font-black uppercase tracking-[0.18em] text-stone-950 transition hover:bg-cyan-200 disabled:opacity-70"
                    disabled={isRefreshing}
                  >
                    <RefreshCw className={`h-4 w-4 ${isRefreshing ? "animate-spin" : ""}`} />
                    <span>Sync</span>
                  </button>
                </div>
              </div>

              <div className="grid border-t border-stone-800 bg-stone-950/75 text-[10px] font-semibold uppercase tracking-[0.22em] text-stone-500 sm:grid-cols-3">
                <div className="flex items-center gap-2 border-b border-stone-800 px-4 py-3 sm:border-b-0 sm:border-r">
                  <Satellite className="h-3.5 w-3.5 text-cyan-300" />
                  Market feed online
                </div>
                <div className="flex items-center gap-2 border-b border-stone-800 px-4 py-3 sm:border-b-0 sm:border-r">
                  <CircleDollarSign className="h-3.5 w-3.5 text-emerald-300" />
                  INR portfolio view
                </div>
                <div className="flex items-center gap-2 px-4 py-3">
                  <Zap className="h-3.5 w-3.5 text-amber-300" />
                  News plus AI context
                </div>
              </div>
            </header>

            <main className="grid flex-1 gap-3 xl:grid-cols-[minmax(0,1fr)_430px]">
              <section className="min-w-0">
                <PortfolioOverview refreshTrigger={refreshTrigger} />
              </section>

              <aside className="min-w-0 xl:sticky xl:top-3 xl:self-start">
                <AskGPTChat />
              </aside>
            </main>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
