from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from db_models import CompletionRow, HabitRow, UserRow
from lib.auth import get_current_user
from lib.dates import today_iso
from models.leaderboard import LeaderboardEntry


router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("", response_model=list[LeaderboardEntry])
async def leaderboard(_: UserRow = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    users = (await session.scalars(select(UserRow))).all()
    rows: list[dict] = []
    today = date.fromisoformat(today_iso())
    for user in users:
        completion_dates = list((await session.scalars(select(CompletionRow.completion_date).where(CompletionRow.user_id == user.id))).all())
        active_habits = await session.scalar(select(func.count(HabitRow.id)).where(HabitRow.user_id == user.id))
        unique_dates = set(completion_dates)
        streak = 0
        cursor = today
        while cursor in unique_dates:
            streak += 1
            cursor -= timedelta(days=1)
        rows.append({"name": user.name, "score": len(unique_dates), "streak": streak, "completed": len(completion_dates), "active_habits": active_habits or 0})
    rows.sort(key=lambda row: (row["score"], row["completed"]), reverse=True)
    return [LeaderboardEntry(rank=index, **row) for index, row in enumerate(rows, 1)]