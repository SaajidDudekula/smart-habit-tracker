import { NavLink } from "react-router-dom";
import "./Sidebar.css";

export default function Sidebar() {
  return (
    <aside className="sidebar">
      {/* Brand */}
      <div className="sidebar-brand">
        <span className="logo-dot" />
        <h1>SmartHabits</h1>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/habits"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Habits
        </NavLink>

        <NavLink
          to="/leaderboard"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Leaderboard
        </NavLink>
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <span>Build consistency.</span>
      </div>
    </aside>
  );
}
