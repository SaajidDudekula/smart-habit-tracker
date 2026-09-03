from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from db_models import CompletionRow, HabitRow, UserRow
from lib.auth import get_current_user, new_id
from lib.dates import today_iso
from models.habits import CompletionRecord, CompletionToggle, DashboardStats, Habit, HabitCreate, HabitUpdate, WeeklyPoint


router = APIRouter(prefix="/habits", tags=["habits"])


def today_date() -> date:
    return date.fromisoformat(today_iso())


async def habit_stats(session: AsyncSession, habit: HabitRow, user_id: str, today: date) -> Habit:
    dates = set((await session.scalars(select(CompletionRow.completion_date).where(CompletionRow.habit_id == habit.id, CompletionRow.user_id == user_id))).all())
    streak = 0
    cursor = today
    while cursor in dates:
        streak += 1
        cursor -= timedelta(days=1)
    return Habit(
        id=habit.id,
        user_id=habit.user_id,
        name=habit.name,
        description=habit.description,
        color=habit.color,
        created_at=habit.created_at,
        current_streak=streak,
        total_completions=len(dates),
        completed_today=today in dates,
    )


@router.get("", response_model=list[Habit])
async def list_habits(user: UserRow = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    habits = (await session.scalars(select(HabitRow).where(HabitRow.user_id == user.id).order_by(HabitRow.created_at))).all()
    today = today_date()
    return [await habit_stats(session, habit, user.id, today) for habit in habits]


@router.post("", response_model=Habit, status_code=status.HTTP_201_CREATED)
async def create_habit(payload: HabitCreate, user: UserRow = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    habit = HabitRow(
        id=new_id(),
        user_id=user.id,
        name=payload.name.strip(),
        description=payload.description.strip(),
        color=payload.color,
        created_at=datetime.now(timezone.utc),
    )
    session.add(habit)
    await session.commit()
    return await habit_stats(session, habit, user.id, today_date())


@router.put("/{habit_id}", response_model=Habit)
async def update_habit(habit_id: str, payload: HabitUpdate, user: UserRow = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    habit = await session.scalar(select(HabitRow).where(HabitRow.id == habit_id, HabitRow.user_id == user.id))
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(habit, key, value.strip() if isinstance(value, str) else value)
    await session.commit()
    return await habit_stats(session, habit, user.id, today_date())


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(habit_id: str, user: UserRow = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    habit = await session.scalar(select(HabitRow).where(HabitRow.id == habit_id, HabitRow.user_id == user.id))
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    await session.delete(habit)
    await session.commit()


@router.post("/{habit_id}/complete", response_model=CompletionToggle)
async def toggle_completion(habit_id: str, user: UserRow = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    habit = await session.scalar(select(HabitRow).where(HabitRow.id == habit_id, HabitRow.user_id == user.id))
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    day = today_date()
    existing = await session.scalar(select(CompletionRow).where(CompletionRow.habit_id == habit_id, CompletionRow.user_id == user.id, CompletionRow.completion_date == day))
    if existing:
        await session.delete(existing)
        await session.commit()
        return CompletionToggle(completed=False, date=day.isoformat(), streak=0)
    session.add(CompletionRow(id=new_id(), habit_id=habit_id, user_id=user.id, completion_date=day))
    await session.commit()
    updated = await habit_stats(session, habit, user.id, day)
    return CompletionToggle(completed=True, date=day.isoformat(), streak=updated.current_streak)


@router.get("/history", response_model=list[CompletionRecord])
async def history(user: UserRow = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    rows = (await session.execute(select(CompletionRow, HabitRow).join(HabitRow, HabitRow.id == CompletionRow.habit_id).where(CompletionRow.user_id == user.id).order_by(CompletionRow.completion_date.desc()))).all()
    return [CompletionRecord(id=item.id, habit_id=item.habit_id, habit_name=habit.name, date=item.completion_date.isoformat(), color=habit.color) for item, habit in rows]


@router.get("/dashboard", response_model=DashboardStats)
async def dashboard(user: UserRow = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    habits = (await session.scalars(select(HabitRow).where(HabitRow.user_id == user.id))).all()
    completions = (await session.scalars(select(CompletionRow).where(CompletionRow.user_id == user.id))).all()
    dates = {item.completion_date for item in completions}
    today = today_date()
    today_completed = sum(1 for item in completions if item.completion_date == today)
    streak = 0
    cursor = today
    while cursor in dates:
        streak += 1
        cursor -= timedelta(days=1)
    weekly: list[WeeklyPoint] = []
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        weekly.append(WeeklyPoint(date=day.isoformat(), label=day.strftime("%a").upper(), completed=sum(1 for item in completions if item.completion_date == day), total=len(habits)))
    total_possible = len(habits) * 7
    week_completed = sum(point.completed for point in weekly)
    return DashboardStats(today_completed=today_completed, today_total=len(habits), active_streak=streak, consistency=round((week_completed / total_possible) * 100) if total_possible else 0, weekly_progress=weekly)