import { useQuery } from "@tanstack/react-query";
import { Crown, Flame, Medal, Trophy } from "lucide-react";
import { apiGet } from "@/lib/api";
import type { LeaderboardEntry } from "@/lib/types";

const rankColors = ["#ffcc00", "#a8b0bd", "#bd7b4b"];
const rankLabels = ["Circle Leader", "Momentum Maker", "Consistency Crew"];
const ordinalLabels = ["1st in your circle", "2nd in your circle", "3rd in your circle"];

export default function Leaderboard() {
  const query = useQuery({ queryKey: ["leaderboard"], queryFn: () => apiGet<LeaderboardEntry[]>("/leaderboard"), retry: false, refetchOnMount: "always", refetchInterval: 15000 });
  const entries = query.data ?? [];
  const podium = entries.slice(0, 3);
  return (
    <div className="mx-auto max-w-[1200px]" data-testid="leaderboard-page">
      <div className="mb-10 flex flex-col justify-between gap-5 md:flex-row md:items-end">
        <div>
          <p className="mb-3 text-[10px] font-bold uppercase tracking-[0.28em] text-[#ff3b30]" data-testid="leaderboard-eyebrow">Your circle / shared momentum</p>
          <h1 className="font-heading text-5xl font-black uppercase leading-none tracking-tight" data-testid="leaderboard-title">Friends ranking.</h1>
          <p className="mt-4 max-w-lg text-sm leading-relaxed text-[#8a8a8e]" data-testid="leaderboard-subtitle">See how your circle is building momentum, celebrate every streak, and keep one another moving.</p>
        </div>
        <div className="flex items-center gap-2 text-xs uppercase tracking-[0.16em] text-[#8a8a8e]" data-testid="leaderboard-season-status"><span className="size-2 rounded-full bg-[#ff3b30]" />Circle rankings</div>
      </div>
      <section className="mb-6 grid gap-px border border-[#262626] bg-[#262626] md:grid-cols-3" data-testid="podium-grid">
        {query.isLoading ? (
          <div className="col-span-3 bg-[#141414] p-10 text-sm text-[#8a8a8e]" data-testid="leaderboard-loading-state">Syncing your live circle...</div>
        ) : podium.length === 0 ? (
          <div className="col-span-3 bg-[#141414] p-10 text-sm text-[#8a8a8e]" data-testid="empty-leaderboard-state">Your circle is ready. Invite friends and build momentum together.</div>
        ) : podium.map((entry, index) => (
          <div className={`relative bg-[#141414] p-7 ${index === 0 ? "md:-translate-y-3 md:pt-10" : ""}`} key={entry.rank} data-testid={`podium-entry-${entry.rank}`}>
            <div className="mb-8 flex items-center justify-between"><span className="font-heading text-5xl font-black" style={{ color: rankColors[index] }}>{String(entry.rank).padStart(2, "0")}</span>{index === 0 ? <Crown size={22} className="text-[#ffcc00]" /> : <Medal size={21} className="text-[#555]" />}</div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.18em]" style={{ color: rankColors[index] }} data-testid={`podium-social-label-${entry.rank}`}>{rankLabels[index]}</p>
            <p className="mt-2 font-heading text-2xl font-black uppercase" data-testid={`podium-name-${entry.rank}`}>{entry.name}</p>
            <p className="mt-2 text-[10px] uppercase tracking-[0.18em] text-[#8a8a8e]" data-testid={`podium-position-${entry.rank}`}>{ordinalLabels[index]} · {entry.streak} day streak · {entry.active_habits} active {entry.active_habits === 1 ? "habit" : "habits"}</p>
            <p className="mt-6 font-mono text-2xl font-bold text-[#007aff]" data-testid={`podium-score-${entry.rank}`}>{entry.score}<span className="ml-2 text-[10px] text-[#8a8a8e]">consistency pts</span></p>
          </div>
        ))}
      </section>
      <section className="border border-[#262626] bg-[#141414]" data-testid="leaderboard-table-panel">
        <div className="flex items-center justify-between border-b border-[#262626] p-6"><div className="flex items-center gap-3"><Trophy size={18} className="text-[#ffcc00]" /><h2 className="font-heading text-2xl font-black uppercase">Your circle</h2></div><span className="font-mono text-xs text-[#8a8a8e]" data-testid="leaderboard-count">{query.isLoading ? "Syncing..." : `${entries.length} people`}</span></div>
        <div className="overflow-x-auto"><table className="w-full min-w-[720px] text-left"><thead className="border-b border-[#262626] text-[10px] uppercase tracking-[0.18em] text-[#555]"><tr><th className="px-6 py-4">Circle rank</th><th className="px-6 py-4">Friend</th><th className="px-6 py-4">Active habits</th><th className="px-6 py-4">Consistency</th><th className="px-6 py-4">Current streak</th><th className="px-6 py-4">Habits kept</th></tr></thead><tbody>{query.isLoading ? <tr><td className="px-6 py-5 text-sm text-[#8a8a8e]" colSpan={6}>Loading live records...</td></tr> : entries.map((entry) => <tr className="border-b border-[#262626] transition-colors hover:bg-[#191919]" key={entry.rank} data-testid={`leaderboard-row-${entry.rank}`}><td className="px-6 py-5 font-mono text-sm text-[#8a8a8e]">#{String(entry.rank).padStart(2, "0")}</td><td className="px-6 py-5 font-semibold" data-testid={`leaderboard-player-${entry.rank}`}>{entry.name}</td><td className="px-6 py-5 font-mono text-sm text-[#8a8a8e]" data-testid={`leaderboard-habits-${entry.rank}`}>{entry.active_habits}</td><td className="px-6 py-5 font-mono text-sm text-[#007aff]">{entry.score} pts</td><td className="px-6 py-5 text-sm text-[#8a8a8e]"><span className="inline-flex items-center gap-2"><Flame size={14} className="text-[#ff3b30]" />{entry.streak} days</span></td><td className="px-6 py-5 font-mono text-sm text-[#8a8a8e]">{entry.completed}</td></tr>)}</tbody></table></div>
      </section>
    </div>
  );
}