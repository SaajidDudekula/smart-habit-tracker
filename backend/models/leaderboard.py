from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    rank: int
    name: str
    score: int
    streak: int
    completed: int
    active_habits: int