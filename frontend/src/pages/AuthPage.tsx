import { useState, type FormEvent } from "react";
import { useMutation } from "@tanstack/react-query";
import { ArrowRight, Check, Flame, LockKeyhole, ShieldCheck, Target } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { apiPost, ApiError } from "@/lib/api";
import { queryClient } from "@/lib/queryClient";
import type { AuthResponse } from "@/lib/types";

type Mode = "login" | "register";

export default function AuthPage() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<Mode>("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const authMutation = useMutation({
    mutationFn: () =>
      mode === "login"
        ? apiPost<AuthResponse>("/auth/login", { email, password })
        : apiPost<AuthResponse>("/auth/register", { name, email, password }),
    onSuccess: ({ user }) => {
      queryClient.setQueryData(["auth", "me"], user);
      toast.success(mode === "login" ? "Welcome back" : "Your account is ready");
      navigate("/");
    },
    onError: (error) => {
      const detail = error instanceof ApiError && typeof error.body === "object" && error.body !== null && "detail" in error.body ? String(error.body.detail) : "Please check your details and try again";
      toast.error(detail);
    },
  });

  const submit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    authMutation.mutate();
  };

  return (
    <main className="min-h-svh bg-[#0a0a0a] text-white" data-testid="auth-page">
      <div className="grid min-h-svh lg:grid-cols-[1.05fr_0.95fr]">
        <section className="relative hidden overflow-hidden border-r border-[#262626] lg:flex lg:flex-col lg:justify-between lg:p-12 xl:p-16" data-testid="auth-brand-panel">
          <div className="absolute left-0 top-0 h-72 w-72 rounded-full bg-[#007aff]/10 blur-3xl" />
          <div className="relative z-10 flex items-center gap-3" data-testid="auth-brand-lockup">
            <div className="grid size-10 place-items-center border border-[#007aff]/50 bg-[#007aff] text-white"><Target size={21} /></div>
            <span className="font-heading text-xl font-bold uppercase tracking-[0.16em]">Habit / OS</span>
          </div>
          <div className="relative z-10 max-w-xl">
            <p className="mb-5 text-xs font-semibold uppercase tracking-[0.3em] text-[#007aff]" data-testid="auth-eyebrow">Consistency command center</p>
            <h1 className="font-heading text-6xl font-black uppercase leading-[0.88] tracking-[-0.045em] xl:text-8xl" data-testid="auth-hero-title">Make the<br /><span className="text-[#007aff]">ordinary</span><br />unstoppable.</h1>
            <p className="mt-8 max-w-md text-base leading-relaxed text-[#8a8a8e]" data-testid="auth-hero-copy">Your daily habits, streak momentum, and competitive edge in one precise operating system.</p>
          </div>
          <div className="relative z-10 grid max-w-xl grid-cols-3 border border-[#262626] bg-[#141414]" data-testid="auth-proof-grid">
            {[{ icon: Flame, value: "07", label: "day streak" }, { icon: Check, value: "92%", label: "consistency" }, { icon: ShieldCheck, value: "100%", label: "private" }].map(({ icon: Icon, value, label }) => (
              <div className="border-r border-[#262626] p-4 last:border-r-0" key={label} data-testid={`auth-proof-${label.replace(" ", "-")}`}>
                <Icon className="mb-5 text-[#007aff]" size={17} />
                <p className="font-mono text-xl font-bold" data-testid={`auth-proof-value-${label.replace(" ", "-")}`}>{value}</p>
                <p className="mt-1 text-[10px] uppercase tracking-[0.16em] text-[#8a8a8e]">{label}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="flex items-center justify-center p-6 sm:p-10 lg:p-16" data-testid="auth-form-panel">
          <div className="w-full max-w-md">
            <div className="mb-10 flex items-center gap-3 lg:hidden" data-testid="auth-mobile-lockup"><div className="grid size-9 place-items-center bg-[#007aff]"><Target size={19} /></div><span className="font-heading text-lg font-bold uppercase tracking-[0.16em]">Habit / OS</span></div>
            <div className="mb-10">
              <p className="mb-3 text-[10px] font-semibold uppercase tracking-[0.25em] text-[#8a8a8e]" data-testid="auth-form-eyebrow">Secure access</p>
              <h2 className="font-heading text-4xl font-black uppercase leading-none tracking-tight" data-testid="auth-form-title">{mode === "login" ? "Resume your run." : "Start your run."}</h2>
              <p className="mt-4 text-sm leading-relaxed text-[#8a8a8e]" data-testid="auth-form-description">{mode === "login" ? "Your next completed habit is waiting." : "Build a private system that compounds."}</p>
            </div>
            <div className="mb-8 grid grid-cols-2 border-b border-[#262626]" data-testid="auth-mode-tabs">
              {(["login", "register"] as Mode[]).map((value) => <button type="button" key={value} onClick={() => setMode(value)} className={`border-b-2 py-3 text-left text-xs font-bold uppercase tracking-[0.18em] transition-colors ${mode === value ? "border-[#007aff] text-white" : "border-transparent text-[#8a8a8e] hover:text-white"}`} data-testid={`auth-${value}-tab-button`}>{value === "login" ? "Sign in" : "Create account"}</button>)}
            </div>
            <form className="space-y-5" onSubmit={submit} data-testid="auth-form">
              {mode === "register" && <label className="block" data-testid="auth-name-field"><span className="mb-2 block text-[10px] font-bold uppercase tracking-[0.2em] text-[#8a8a8e]">Name</span><Input required value={name} onChange={(event) => setName(event.target.value)} placeholder="Your name" className="h-12 rounded-none border-[#262626] bg-[#141414] text-white placeholder:text-[#555]" data-testid="auth-name-input" /></label>}
              <label className="block" data-testid="auth-email-field"><span className="mb-2 block text-[10px] font-bold uppercase tracking-[0.2em] text-[#8a8a8e]">Email</span><Input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" className="h-12 rounded-none border-[#262626] bg-[#141414] text-white placeholder:text-[#555]" data-testid="auth-email-input" /></label>
              <label className="block" data-testid="auth-password-field"><span className="mb-2 block text-[10px] font-bold uppercase tracking-[0.2em] text-[#8a8a8e]">Password</span><Input required minLength={8} type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="8+ characters" className="h-12 rounded-none border-[#262626] bg-[#141414] text-white placeholder:text-[#555]" data-testid="auth-password-input" /></label>
              <Button type="submit" disabled={authMutation.isPending} className="h-12 w-full rounded-none bg-[#007aff] font-bold uppercase tracking-[0.16em] text-white hover:bg-[#1990ff] hover:text-white" data-testid="auth-submit-button">{authMutation.isPending ? "Working..." : mode === "login" ? "Enter workspace" : "Create workspace"}<ArrowRight size={17} /></Button>
            </form>
            <div className="mt-10 flex items-center gap-3 border-t border-[#262626] pt-5 text-xs text-[#8a8a8e]" data-testid="auth-security-note"><LockKeyhole size={15} className="text-[#007aff]" />JWT-protected. Your progress is yours.</div>
          </div>
        </section>
      </div>
    </main>
  );
}