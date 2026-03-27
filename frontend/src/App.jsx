import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Auth from "./pages/Auth";
import Dashboard from "./pages/Dashboard";
import Habits from "./pages/Habits";
import Leaderboard from "./pages/Leaderboard";
import "./App.css";

/* -----------------------------
   AUTH UTILITIES (LOCAL)
----------------------------- */

function isAuthenticated() {
  return !!localStorage.getItem("token");
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  window.location.href = "/";
}

/* -----------------------------
   PROTECTED ROUTE
----------------------------- */

function ProtectedRoute({ children }) {
  if (!isAuthenticated()) {
    return <Navigate to="/" replace />;
  }
  return children;
}

/* -----------------------------
   MAIN LAYOUT (INLINE HEADER)
----------------------------- */

function AppLayout({ children }) {
  const location = useLocation();

  const pageTitleMap = {
    "/dashboard": "Dashboard",
    "/habits": "Habits",
    "/leaderboard": "Leaderboard",
  };

  const title = pageTitleMap[location.pathname] || "";

  return (
    <div className="app-shell">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Area */}
      <div className="app-main">
        {/* Inline Header */}
        <header className="app-header">
          <h2>{title}</h2>
          <button className="logout-btn" onClick={logout}>
            Logout
          </button>
        </header>

        {/* Page Content */}
        <div className="app-content">{children}</div>
      </div>
    </div>
  );
}

/* -----------------------------
   APP ROOT
----------------------------- */

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Auth */}
        <Route path="/" element={<Auth />} />

        {/* Protected Pages */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <AppLayout>
                <Dashboard />
              </AppLayout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/habits"
          element={
            <ProtectedRoute>
              <AppLayout>
                <Habits />
              </AppLayout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/leaderboard"
          element={
            <ProtectedRoute>
              <AppLayout>
                <Leaderboard />
              </AppLayout>
            </ProtectedRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}
