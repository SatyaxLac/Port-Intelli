import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import StockCard from "@/components/StockCard";
import { Skeleton } from "@/components/ui/skeleton";
import { useToast } from "@/hooks/use-toast";
import { fetchPortfolio } from "@/lib/api";
import {
  AlertTriangle,
  BarChart3,
  Layers3,
  LineChart,
  TrendingDown,
  TrendingUp,
  Wallet,
} from "lucide-react";

interface PortfolioOverviewProps {
  refreshTrigger: number;
}

const PortfolioOverview = ({ refreshTrigger }: PortfolioOverviewProps) => {
  const { toast } = useToast();

  const { data: portfolio, isLoading, error } = useQuery({
    queryKey: ["portfolio", refreshTrigger],
    queryFn: fetchPortfolio,
    staleTime: 60000,
    retry: 1,
  });

  useEffect(() => {
    if (error) {
      toast({
        title: "Error loading portfolio",
        description: "Could not connect to portfolio service.",
        variant: "destructive",
      });
    }
  }, [error, toast]);

  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);

  const formatPercentage = (pct: number | undefined) => {
    if (pct === undefined || pct === null) return "0.00%";
    return `${pct >= 0 ? "+" : ""}${pct.toFixed(2)}%`;
  };

  const calcPct = (total: number, gain: number) => (!total ? 0 : (gain / total) * 100);

  if (isLoading) {
    return (
      <div className="space-y-3">
        <section className="panel-edge p-4 lg:p-5">
          <Skeleton className="h-4 w-32 rounded-none bg-stone-800" />
          <Skeleton className="mt-5 h-16 w-2/3 rounded-none bg-stone-800" />
          <div className="mt-6 grid gap-3 sm:grid-cols-3">
            {[...Array(3)].map((_, i) => (
              <Skeleton key={i} className="h-24 rounded-none bg-stone-800" />
            ))}
          </div>
        </section>
        {[...Array(4)].map((_, i) => (
          <Skeleton key={i} className="h-32 rounded-none border border-stone-800 bg-stone-900" />
        ))}
      </div>
    );
  }

  if (error || !portfolio) {
    return (
      <section className="panel-edge grid min-h-[420px] place-items-center p-8 text-center">
        <div>
          <div className="mx-auto grid h-14 w-14 place-items-center border border-rose-300/50 bg-rose-400/10">
            <AlertTriangle className="h-7 w-7 text-rose-300" />
          </div>
          <h3 className="mt-5 text-xl font-black text-stone-100">Unable to load portfolio</h3>
          <p className="mt-2 text-sm text-stone-500">Ensure the API server is running on port 8000.</p>
        </div>
      </section>
    );
  }

  const netPct = calcPct(portfolio.total_invested, portfolio.net_gain);
  const isPositive = portfolio.net_gain >= 0;
  const trendTone = isPositive ? "text-emerald-300" : "text-rose-300";
  const trendBg = isPositive ? "bg-emerald-300" : "bg-rose-300";
  const exposure = portfolio.total_invested ? Math.min(Math.abs(netPct), 100) : 0;
  const sortedByGain = [...portfolio.stocks].sort((a, b) => (b.gain || 0) - (a.gain || 0));
  const strongest = sortedByGain[0];
  const weakest = sortedByGain[sortedByGain.length - 1];

  const metrics = [
    {
      label: "Invested",
      value: formatCurrency(portfolio.total_invested),
      icon: Wallet,
      tone: "text-amber-300",
    },
    {
      label: "Current value",
      value: formatCurrency(portfolio.total_current),
      icon: BarChart3,
      tone: "text-cyan-300",
    },
    {
      label: "Holdings",
      value: portfolio.stocks.length.toString(),
      icon: Layers3,
      tone: "text-stone-200",
    },
  ];

  return (
    <div className="space-y-3">
      <section className="grid gap-3 lg:grid-cols-[minmax(0,1.35fr)_minmax(280px,0.65fr)]">
        <div className="panel-edge overflow-hidden">
          <div className="border-b border-stone-800 px-4 py-3">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <LineChart className="h-4 w-4 text-cyan-300" />
                <span className="text-[10px] font-bold uppercase tracking-[0.28em] text-stone-500">
                  Portfolio return
                </span>
              </div>
              <span className={`font-mono text-xs font-bold ${trendTone}`}>
                {formatPercentage(netPct)}
              </span>
            </div>
          </div>

          <div className="p-4 sm:p-5 lg:p-6">
            <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-stone-500">
                  Net return
                </p>
                <div className="mt-3 flex flex-wrap items-end gap-3">
                  <h2 className={`font-mono text-4xl font-black leading-none sm:text-6xl ${trendTone}`}>
                    {formatCurrency(portfolio.net_gain)}
                  </h2>
                  <div className={`mb-1 inline-flex items-center gap-1.5 border px-2.5 py-1 text-xs font-black uppercase tracking-[0.16em] ${
                    isPositive
                      ? "border-emerald-300/40 bg-emerald-300/10 text-emerald-200"
                      : "border-rose-300/40 bg-rose-300/10 text-rose-200"
                  }`}>
                    {isPositive ? <TrendingUp className="h-3.5 w-3.5" /> : <TrendingDown className="h-3.5 w-3.5" />}
                    {isPositive ? "Gain" : "Drawdown"}
                  </div>
                </div>
              </div>

              <div className="min-w-[190px] border border-stone-800 bg-stone-950/70 p-3">
                <div className="flex items-center justify-between text-[10px] font-bold uppercase tracking-[0.2em] text-stone-500">
                  <span>Move scale</span>
                  <span>{formatPercentage(netPct)}</span>
                </div>
                <div className="mt-3 h-2 bg-stone-800">
                  <div className={`h-full ${trendBg}`} style={{ width: `${exposure}%` }} />
                </div>
              </div>
            </div>

            <div className="mt-6 grid gap-3 sm:grid-cols-3">
              {metrics.map((metric) => (
                <div key={metric.label} className="metric-tile p-4">
                  <div className="flex items-center justify-between gap-3">
                    <span className="text-[10px] font-bold uppercase tracking-[0.22em] text-stone-500">
                      {metric.label}
                    </span>
                    <metric.icon className={`h-4 w-4 ${metric.tone}`} />
                  </div>
                  <p className="mt-4 truncate font-mono text-lg font-black text-stone-100">
                    {metric.value}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="panel-edge flex flex-col justify-between p-4 sm:p-5">
          <div>
            <p className="text-[10px] font-bold uppercase tracking-[0.28em] text-stone-500">
              Position scan
            </p>
            <div className="mt-5 space-y-4">
              <div className="border-l-2 border-emerald-300 pl-3">
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-stone-500">
                  Strongest
                </p>
                <p className="mt-1 font-mono text-lg font-black text-stone-100">
                  {strongest?.symbol || "N/A"}
                </p>
                <p className="text-sm text-emerald-300">
                  {strongest ? formatCurrency(strongest.gain || 0) : formatCurrency(0)}
                </p>
              </div>
              <div className="border-l-2 border-rose-300 pl-3">
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-stone-500">
                  Weakest
                </p>
                <p className="mt-1 font-mono text-lg font-black text-stone-100">
                  {weakest?.symbol || "N/A"}
                </p>
                <p className="text-sm text-rose-300">
                  {weakest ? formatCurrency(weakest.gain || 0) : formatCurrency(0)}
                </p>
              </div>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-8 gap-1">
            {portfolio.stocks.slice(0, 24).map((stock) => {
              const gain = stock.gain !== undefined ? stock.gain : stock.gain_loss || 0;
              return (
                <div
                  key={stock.symbol}
                  className={`h-8 border ${gain >= 0 ? "border-emerald-300/30 bg-emerald-300/15" : "border-rose-300/30 bg-rose-300/15"}`}
                  title={`${stock.symbol}: ${formatCurrency(gain)}`}
                />
              );
            })}
          </div>
        </div>
      </section>

      <section className="panel-edge overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-stone-800 px-4 py-3">
          <div>
            <h2 className="text-sm font-black uppercase tracking-[0.24em] text-stone-200">
              Holdings matrix
            </h2>
            <p className="mt-1 text-xs text-stone-500">
              {portfolio.stocks.length} active position{portfolio.stocks.length !== 1 ? "s" : ""}
            </p>
          </div>
          <div className="hidden grid-cols-3 gap-2 text-[10px] font-bold uppercase tracking-[0.18em] text-stone-500 sm:grid">
            <span>Cost</span>
            <span>Value</span>
            <span>Signal</span>
          </div>
        </div>

        <div className="divide-y divide-stone-800/80">
          {portfolio.stocks.map((stock, i) => (
            <div key={stock.symbol} className="animate-slide-up" style={{ animationDelay: `${i * 45}ms` }}>
              <StockCard stock={stock} />
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default PortfolioOverview;
