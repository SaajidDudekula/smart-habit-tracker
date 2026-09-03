import { Navigate, Route, Routes } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { User } from "@/lib/types";
import AppLayout from "@/components/AppLayout";
import AuthPage from "@/pages/AuthPage";
import Dashboard from "@/pages/Dashboard";
import History from "@/pages/History";
import Leaderboard from "@/pages/Leaderboard";

export default function App() {
  const userQuery = useQuery({ queryKey: ["auth", "me"], queryFn: () => apiGet<User | null>("/api/auth/me"), retry: false });
  const user = userQuery.data;
  return <><Routes><Route path="/auth" element={<AuthPage />} /><Route element={userQuery.isLoading ? <LoadingShell /> : user ? <AppLayout user={user} /> : <Navigate to="/auth" replace />}><Route path="/" element={<Dashboard />} /><Route path="/history" element={<History />} /><Route path="/leaderboard" element={<Leaderboard />} /></Route><Route path="*" element={<Navigate to="/" replace />} /></Routes><Toaster position="bottom-right" richColors /></>;
}

function LoadingShell() {
  return <div className="grid min-h-svh place-items-center bg-[#0a0a0a] text-[#8a8a8e]" data-testid="loading-shell"><div className="text-center"><div className="mx-auto mb-4 size-7 animate-pulse bg-[#007aff]" /><p className="text-[10px] font-bold uppercase tracking-[0.24em]">Loading workspace</p></div></div>;
}
