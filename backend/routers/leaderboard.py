from fastapi import APIRouter, Depends

from lib.auth import get_current_user
from lib.db import db
from models.leaderboard import LeaderboardEntry


router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("", response_model=list[LeaderboardEntry])
async def leaderboard(_: dict = Depends(get_current_user)):
    users = await db.users.find({}, {"id": 1, "name": 1}).to_list(1000)
    rows = []
    for user in users:
        completions = await db.completions.find({"user_id": user["id"]}, {"date": 1, "_id": 0}).to_list(5000)
        unique_dates = {item["date"] for item in completions}
        rows.append({"name": user["name"], "score": len(unique_dates), "streak": 0, "completed": len(completions)})
    rows.sort(key=lambda row: (row["score"], row["completed"]), reverse=True)
    return [LeaderboardEntry(rank=index, **row) for index, row in enumerate(rows, 1)]