from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from lib.auth import get_current_user, new_id
from lib.dates import today_iso
from lib.db import db
from models.habits import CompletionRecord, CompletionToggle, DashboardStats, Habit, HabitCreate, HabitUpdate, WeeklyPoint


router = APIRouter(prefix="/habits", tags=["habits"])


async def habit_stats(habit: dict, user_id: str, today: str) -> Habit:
    completions = await db.completions.find({"habit_id": habit["id"], "user_id": user_id}, {"date": 1, "_id": 0}).to_list(5000)
    completed_dates = {item["date"] for item in completions}
    streak = 0
    cursor = datetime.strptime(today, "%Y-%m-%d").date()
    while cursor.strftime("%Y-%m-%d") in completed_dates:
        streak += 1
        cursor -= timedelta(days=1)
    return Habit(
        **{key: habit[key] for key in ("id", "user_id", "name", "description", "color", "created_at")},
        current_streak=streak,
        total_completions=len(completed_dates),
        completed_today=today in completed_dates,
    )


@router.get("", response_model=list[Habit])
async def list_habits(user: dict = Depends(get_current_user)):
    today = today_iso()
    habits = await db.habits.find({"user_id": user["id"]}).sort("created_at", 1).to_list(200)
    return [await habit_stats(habit, user["id"], today) for habit in habits]


@router.post("", response_model=Habit, status_code=status.HTTP_201_CREATED)
async def create_habit(payload: HabitCreate, user: dict = Depends(get_current_user)):
    habit = {
        "id": new_id(),
        "user_id": user["id"],
        "name": payload.name.strip(),
        "description": payload.description.strip(),
        "color": payload.color,
        "created_at": datetime.now(timezone.utc),
    }
    await db.habits.insert_one(habit)
    return await habit_stats(habit, user["id"], today_iso())


@router.put("/{habit_id}", response_model=Habit)
async def update_habit(habit_id: str, payload: HabitUpdate, user: dict = Depends(get_current_user)):
    habit = await db.habits.find_one({"id": habit_id, "user_id": user["id"]})
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    updates = {key: value.strip() if isinstance(value, str) else value for key, value in payload.model_dump(exclude_none=True).items()}
    if updates:
        await db.habits.update_one({"id": habit_id}, {"$set": updates})
        habit.update(updates)
    return await habit_stats(habit, user["id"], today_iso())


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(habit_id: str, user: dict = Depends(get_current_user)):
    result = await db.habits.delete_one({"id": habit_id, "user_id": user["id"]})
    if not result.deleted_count:
        raise HTTPException(status_code=404, detail="Habit not found")
    await db.completions.delete_many({"habit_id": habit_id, "user_id": user["id"]})


@router.post("/{habit_id}/complete", response_model=CompletionToggle)
async def toggle_completion(habit_id: str, user: dict = Depends(get_current_user)):
    habit = await db.habits.find_one({"id": habit_id, "user_id": user["id"]})
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    date = today_iso()
    existing = await db.completions.find_one({"habit_id": habit_id, "user_id": user["id"], "date": date})
    if existing:
        await db.completions.delete_one({"id": existing["id"]})
        return CompletionToggle(completed=False, date=date, streak=0)
    await db.completions.insert_one({"id": new_id(), "habit_id": habit_id, "user_id": user["id"], "date": date})
    updated = await habit_stats(habit, user["id"], date)
    return CompletionToggle(completed=True, date=date, streak=updated.current_streak)


@router.get("/history", response_model=list[CompletionRecord])
async def history(user: dict = Depends(get_current_user)):
    items = await db.completions.find({"user_id": user["id"]}).sort("date", -1).to_list(5000)
    result: list[CompletionRecord] = []
    for item in items:
        habit = await db.habits.find_one({"id": item["habit_id"]}, {"name": 1, "color": 1})
        if habit:
            result.append(CompletionRecord(id=item["id"], habit_id=item["habit_id"], habit_name=habit["name"], date=item["date"], color=habit["color"]))
    return result


@router.get("/dashboard", response_model=DashboardStats)
async def dashboard(user: dict = Depends(get_current_user)):
    habits = await db.habits.find({"user_id": user["id"]}).to_list(200)
    completions = await db.completions.find({"user_id": user["id"]}).to_list(5000)
    dates = {item["date"] for item in completions}
    today = today_iso()
    today_completed = sum(1 for item in completions if item["date"] == today)
    streak = 0
    cursor = datetime.strptime(today, "%Y-%m-%d").date()
    while cursor.strftime("%Y-%m-%d") in dates:
        streak += 1
        cursor -= timedelta(days=1)
    weekly: list[WeeklyPoint] = []
    today_date = datetime.strptime(today, "%Y-%m-%d").date()
    for offset in range(6, -1, -1):
        day = today_date - timedelta(days=offset)
        date_str = day.strftime("%Y-%m-%d")
        weekly.append(WeeklyPoint(date=date_str, label=day.strftime("%a").upper(), completed=sum(1 for item in completions if item["date"] == date_str), total=len(habits)))
    total_possible = len(habits) * 7
    week_completed = sum(point.completed for point in weekly)
    return DashboardStats(today_completed=today_completed, today_total=len(habits), active_streak=streak, consistency=round((week_completed / total_possible) * 100) if total_possible else 0, weekly_progress=weekly)