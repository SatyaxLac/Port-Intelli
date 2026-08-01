import { ArrowDownRight, ArrowUpRight, BrainCircuit } from "lucide-react";
import type { Stock } from "@/lib/types";

interface StockCardProps {
  stock: Stock;
}

const StockCard = ({ stock }: StockCardProps) => {
  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);

  const formatPercentage = (percentage: number | undefined) => {
    if (percentage === undefined || percentage === null) return "0.00%";
    return `${percentage >= 0 ? "+" : ""}${percentage.toFixed(2)}%`;
  };

  const gainAmount = stock.gain !== undefined ? stock.gain : stock.gain_loss || 0;
  const isGain = gainAmount >= 0;
  const computedPercentage =
    stock.gain_loss_percentage !== undefined
      ? stock.gain_loss_percentage
      : stock.invested > 0
        ? (gainAmount / stock.invested) * 100
        : 0;

  return (
    <article className="group bg-stone-950/50 px-4 py-4 transition hover:bg-stone-900/80">
      <div className="grid gap-4 lg:grid-cols-[minmax(0,1.35fr)_0.72fr_0.72fr_0.82fr] lg:items-center">
        <div className="min-w-0">
          <div className="flex items-start gap-3">
            <div className={`grid h-11 w-11 shrink-0 place-items-center border font-mono text-xs font-black ${
              isGain
                ? "border-emerald-300/50 bg-emerald-300/10 text-emerald-200"
                : "border-rose-300/50 bg-rose-300/10 text-rose-200"
            }`}>
              {stock.symbol.slice(0, 2)}
            </div>
            <div className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <h3 className="truncate font-mono text-lg font-black tracking-normal text-stone-100">
                  {stock.symbol}
                </h3>
                <span className="border border-stone-700 px-2 py-0.5 text-[10px] font-bold uppercase tracking-[0.18em] text-stone-500">
                  Qty {stock.quantity ?? "-"}
                </span>
              </div>
              <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-stone-500">
                <span>Avg {stock.avg_price ? formatCurrency(stock.avg_price) : "-"}</span>
                <span>Last {stock.current_price ? formatCurrency(stock.current_price) : "-"}</span>
              </div>
            </div>
          </div>
        </div>

        <div>
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-stone-500">Invested</p>
          <p className="mt-1 font-mono text-sm font-black text-stone-100">
            {formatCurrency(stock.invested)}
          </p>
        </div>

        <div>
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-stone-500">Current</p>
          <p className="mt-1 font-mono text-sm font-black text-stone-100">
            {formatCurrency(stock.current_value)}
          </p>
        </div>

        <div className="flex flex-col gap-3">
          <div className={`inline-flex w-fit items-center gap-2 border px-2.5 py-1 font-mono text-xs font-black ${
            isGain
              ? "border-emerald-300/40 bg-emerald-300/10 text-emerald-200"
              : "border-rose-300/40 bg-rose-300/10 text-rose-200"
          }`}>
            {isGain ? <ArrowUpRight className="h-3.5 w-3.5" /> : <ArrowDownRight className="h-3.5 w-3.5" />}
            <span>{formatCurrency(gainAmount)}</span>
            <span>{formatPercentage(computedPercentage)}</span>
          </div>
        </div>
      </div>

      {stock.insight && (
        <div className="mt-4 grid gap-3 border-t border-stone-800 pt-4 sm:grid-cols-[28px_minmax(0,1fr)]">
          <BrainCircuit className="h-4 w-4 text-amber-300" />
          <p className="min-w-0 text-sm leading-6 text-stone-400">{stock.insight}</p>
        </div>
      )}
    </article>
  );
};

export default StockCard;
