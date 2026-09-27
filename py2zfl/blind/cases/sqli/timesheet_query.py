from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import text

from lib.db import engine

app = FastAPI()


class TimesheetQuery(BaseModel):
    group_by: Literal["project", "employee", "week"] = "project"
    direction: Literal["asc", "desc"] = "desc"
    top: int = Field(10, ge=1, le=500)


@app.post("/timesheets/summary")
def timesheet_summary(q: TimesheetQuery):
    stmt = (
        f"SELECT {q.group_by}, SUM(hours) AS hours FROM timesheet_entries "
        f"GROUP BY {q.group_by} ORDER BY hours {q.direction} LIMIT {q.top}"
    )
    with engine.connect() as conn:
        rows = conn.execute(text(stmt)).all()
    return [{"key": k, "hours": float(h)} for k, h in rows]
