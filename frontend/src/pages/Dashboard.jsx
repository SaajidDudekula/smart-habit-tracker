import { useEffect, useRef, useState } from "react";
import "./Dashboard.css";

const API_BASE = "http://localhost:8000";

export default function Dashboard() {
  const [totalHabits, setTotalHabits] = useState(0);
  const [completedToday, setCompletedToday] = useState(0);
  const [completionRate, setCompletionRate] = useState(0);

  const token = localStorage.getItem("token");

  /* ======================================================
     AUTO GREET (ONCE PER SESSION)
  ====================================================== */

useEffect(() => {
  // Play greeting only once per browser session
  if (sessionStorage.getItem("dashboard_greeted")) return;

  const audio = new Audio("/audio/greeting.mp3");
  audio.volume = 1.0; // immediate sound, no fade

  const timer = setTimeout(() => {
    audio
      .play()
      .then(() => {
        sessionStorage.setItem("dashboard_greeted", "true");
      })
      .catch(() => {
        // Edge may block if tab/site is muted – fail silently
      });
  }, 2000); // ⏱️ 2-second delay (as requested)

  return () => clearTimeout(timer);
}, []);

  /* ======================================================
     FETCH DASHBOARD DATA
  ====================================================== */

  useEffect(() => {
    fetchDashboardData();

    const handler = () => fetchDashboardData();
    window.addEventListener("habits-updated", handler);

    return () => window.removeEventListener("habits-updated", handler);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/habits`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = await res.json();
      const habits = Array.isArray(data.habits) ? data.habits : [];

      const total = habits.length;
      const completed = habits.filter(h => h.completed_today).length;
      const rate = total === 0 ? 0 : Math.round((completed / total) * 100);

      setTotalHabits(total);
      setCompletedToday(completed);
      setCompletionRate(rate);
    } catch (err) {
      console.error("Dashboard fetch failed:", err);
      setTotalHabits(0);
      setCompletedToday(0);
      setCompletionRate(0);
    }
  };

  /* ======================================================
     PROGRESS RING CALCULATION
  ====================================================== */

  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  const offset =
    circumference - (completionRate / 100) * circumference;

  /* ======================================================
     UI
  ====================================================== */

  return (
    <div className="dashboard-page">
      <p className="subtitle">Your daily progress overview</p>

      <div className="stats-grid">
        {/* TOTAL HABITS */}
        <div className="panel">
          <span className="panel-label">Total Habits</span>
          <span className="panel-value">{totalHabits}</span>
        </div>

        {/* COMPLETED TODAY */}
        <div className="panel">
          <span className="panel-label">Completed Today</span>
          <span className="panel-value">{completedToday}</span>
        </div>

        {/* COMPLETION RATE */}
        <div className="panel panel-wide">
          <div className="completion-panel">
            <div className="progress-ring">
              <svg width="120" height="120">
                <circle
                  className="ring-bg"
                  cx="60"
                  cy="60"
                  r={radius}
                  strokeWidth="10"
                />
                <circle
                  className="ring-progress"
                  cx="60"
                  cy="60"
                  r={radius}
                  strokeWidth="10"
                  style={{
                    strokeDasharray: circumference,
                    strokeDashoffset: offset
                  }}
                />
              </svg>
              <div className="progress-text">{completionRate}%</div>
            </div>

            <div className="completion-info">
              <h3>Completion Rate</h3>
              <p>
                You completed <strong>{completedToday}</strong> out of{" "}
                <strong>{totalHabits}</strong> habits today.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
