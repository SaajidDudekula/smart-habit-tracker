from datetime import datetime
from pydantic import BaseModel, Field


class HabitCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    description: str = Field(default="", max_length=240)
    color: str = Field(default="#007AFF", pattern=r"^#[0-9A-Fa-f]{6}$")


class HabitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = Field(default=None, max_length=240)
    color: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")


class Habit(BaseModel):
    id: str
    user_id: str
    name: str
    description: str
    color: str
    created_at: datetime
    current_streak: int = 0
    total_completions: int = 0
    completed_today: bool = False


class CompletionToggle(BaseModel):
    completed: bool
    date: str
    streak: int


class CompletionRecord(BaseModel):
    id: str
    habit_id: str
    habit_name: str
    date: str
    color: str


class WeeklyPoint(BaseModel):
    date: str
    label: str
    completed: int
    total: int


class DashboardStats(BaseModel):
    today_completed: int
    today_total: int
    active_streak: int
    consistency: int
    weekly_progress: list[WeeklyPoint]