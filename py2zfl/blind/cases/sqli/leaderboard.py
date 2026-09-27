from enum import Enum

from fastapi import FastAPI
from sqlalchemy import text

from lib.db import engine

app = FastAPI()


class RankBy(str, Enum):
    score = "score"
    wins = "wins"
    streak = "longest_streak"


@app.get("/leaderboard")
def leaderboard(rank_by: RankBy = RankBy.score, limit: int = 20):
    sql = f"SELECT player, {rank_by.value} FROM player_stats ORDER BY {rank_by.value} DESC LIMIT {limit}"
    with engine.connect() as conn:
        rows = conn.execute(text(sql)).all()
    return [{"player": p, rank_by.value: v} for p, v in rows]
