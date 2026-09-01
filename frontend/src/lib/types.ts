export interface User {
  id: string;
  name: string;
  email: string;
}

export interface AuthResponse {
  user: User;
}

export interface Habit {
  id: string;
  user_id: string;
  name: string;
  description: string;
  color: string;
  created_at: string;
  current_streak: number;
  total_completions: number;
  completed_today: boolean;
}

export interface CompletionToggle {
  completed: boolean;
  date: string;
  streak: number;
}

export interface CompletionRecord {
  id: string;
  habit_id: string;
  habit_name: string;
  date: string;
  color: string;
}

export interface WeeklyPoint {
  date: string;
  label: string;
  completed: number;
  total: number;
}

export interface DashboardStats {
  today_completed: number;
  today_total: number;
  active_streak: number;
  consistency: number;
  weekly_progress: WeeklyPoint[];
}

export interface LeaderboardEntry {
  rank: number;
  name: string;
  score: number;
  streak: number;
  completed: number;
}