import { useEffect, useState } from "react";
import "./Leaderboard.css";

const API_BASE = "http://localhost:8000";

export default function Leaderboard() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();

    const handler = () => fetchLeaderboard();
    window.addEventListener("habits-updated", handler);

    return () => window.removeEventListener("habits-updated", handler);
  }, []);

  // ==============================
  // FETCH LEADERBOARD (SAFE)
  // ==============================
  const fetchLeaderboard = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/leaderboard`);
      const data = await res.json();

      setRows(Array.isArray(data.leaderboard) ? data.leaderboard : []);
    } catch (err) {
      console.error("Leaderboard fetch failed:", err);
      setRows([]);
    } finally {
      setLoading(false);
    }
  };

  // ==============================
  // UI
  // ==============================
  return (
    <div className="leaderboard-page">
      <h1>Leaderboard</h1>
      <p className="subtitle">Top performers based on consistency</p>

      {loading ? (
        <p className="loading">Loading leaderboard…</p>
      ) : rows.length === 0 ? (
        <div className="empty-state">
          <p>No leaderboard data yet.</p>
          <span>Complete habits to appear here.</span>
        </div>
      ) : (
        <div className="leaderboard-table">
          <div className="table-header">
            <span>Rank</span>
            <span>User</span>
            <span>Habits</span>
            <span>Total</span>
            <span>Today</span>
          </div>

          {rows.map((r) => (
            <div className="table-row" key={r.name + r.total_completions}>
              <span className="rank">
                {r.rank === 1 ? "🥇" : r.rank === 2 ? "🥈" : r.rank === 3 ? "🥉" : r.rank}
              </span>
              <span className="user">{r.name}</span>
              <span>{r.total_habits}</span>
              <span>{r.total_completions}</span>
              <span className={r.today_completions > 0 ? "today-active" : ""}>
                {r.today_completions}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
