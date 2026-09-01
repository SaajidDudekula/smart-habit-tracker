import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { BarChart3, CalendarDays, CheckSquare, LogOut, Menu, Trophy, X } from "lucide-react";
import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { apiPost } from "@/lib/api";
import { queryClient } from "@/lib/queryClient";
import type { User } from "@/lib/types";

const links = [
  { to: "/", label: "Overview", icon: BarChart3 },
  { to: "/history", label: "History", icon: CalendarDays },
  { to: "/leaderboard", label: "Leaderboard", icon: Trophy },
];

export default function AppLayout({ user }: { user: User }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const logout = useMutation({
    mutationFn: () => apiPost<{ message: string }>("/auth/logout"),
    onSuccess: () => {
      queryClient.clear();
      toast.success("Signed out");
      navigate("/auth");
    },
  });

  return <div className="min-h-svh bg-[#0a0a0a] text-white" data-testid="app-shell">
    <aside className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-[#262626] bg-[#0f0f10] p-6 transition-transform duration-200 lg:translate-x-0 ${mobileOpen ? "translate-x-0" : "-translate-x-full"}`} data-testid="sidebar">
      <div className="flex items-center justify-between" data-testid="sidebar-brand"><div className="flex items-center gap-3"><div className="grid size-9 place-items-center bg-[#007aff] text-white"><CheckSquare size={18} /></div><span className="font-heading text-lg font-bold uppercase tracking-[0.15em]">Habit / OS</span></div><button className="text-[#8a8a8e] lg:hidden" onClick={() => setMobileOpen(false)} data-testid="sidebar-close-button" aria-label="Close navigation"><X size={19} /></button></div>
      <div className="mt-16" data-testid="sidebar-nav-group"><p className="mb-4 text-[10px] font-bold uppercase tracking-[0.25em] text-[#555]">Workspace</p><nav className="space-y-1" data-testid="primary-navigation">{links.map(({ to, label, icon: Icon }) => <NavLink key={to} end={to === "/"} to={to} onClick={() => setMobileOpen(false)} className={({ isActive }) => `group flex items-center gap-3 border-l-2 px-3 py-3 text-sm font-medium transition-[background-color,color,border-color] ${isActive ? "border-[#007aff] bg-[#007aff]/10 text-white" : "border-transparent text-[#8a8a8e] hover:border-[#007aff]/50 hover:bg-[#141414] hover:text-white"}`} data-testid={`nav-${label.toLowerCase()}-link`}><Icon size={17} /><span>{label}</span></NavLink>)}</nav></div>
      <div className="mt-auto border-t border-[#262626] pt-5" data-testid="sidebar-account"><div className="mb-5 flex items-center gap-3"><div className="grid size-9 place-items-center bg-[#242424] font-heading text-lg font-bold text-[#007aff]" data-testid="user-avatar">{user.name.charAt(0).toUpperCase()}</div><div className="min-w-0"><p className="truncate text-sm font-semibold" data-testid="user-name">{user.name}</p><p className="truncate text-[10px] uppercase tracking-[0.1em] text-[#8a8a8e]" data-testid="user-email">{user.email}</p></div></div><Button variant="ghost" onClick={() => logout.mutate()} disabled={logout.isPending} className="h-9 w-full justify-start rounded-none px-3 text-[#8a8a8e] hover:bg-[#1a1a1a] hover:text-white" data-testid="logout-button"><LogOut size={16} />{logout.isPending ? "Signing out..." : "Sign out"}</Button></div>
    </aside>
    {mobileOpen && <button className="fixed inset-0 z-30 bg-black/70 lg:hidden" onClick={() => setMobileOpen(false)} data-testid="mobile-nav-overlay" aria-label="Close menu" />}
    <div className="lg:pl-64"><header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-[#262626] bg-[#0a0a0a]/95 px-5 backdrop-blur lg:px-10" data-testid="topbar"><button className="text-[#8a8a8e] hover:text-white lg:hidden" onClick={() => setMobileOpen(true)} data-testid="mobile-menu-button" aria-label="Open menu"><Menu size={21} /></button><div className="hidden text-[10px] font-bold uppercase tracking-[0.25em] text-[#555] lg:block" data-testid="topbar-breadcrumb">Habit / OS <span className="mx-2 text-[#007aff]">/</span> Daily command</div><div className="ml-auto flex items-center gap-3 text-[10px] uppercase tracking-[0.16em] text-[#8a8a8e]" data-testid="topbar-status"><span className="size-1.5 rounded-full bg-[#007aff]" />System live</div></header><main className="px-5 py-8 lg:px-10 lg:py-12" data-testid="main-content"><Outlet /></main></div>
  </div>;
}