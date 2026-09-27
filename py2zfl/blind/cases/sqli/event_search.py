from typing import Optional

from fastapi import Depends, FastAPI, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from lib.db import engine

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


class EventFilters:
    def __init__(
        self,
        q: Optional[str] = Query(None, max_length=100),
        venue: Optional[str] = None,
        limit: int = Query(25, le=100),
    ):
        self.q = q
        self.venue = venue
        self.limit = limit


@app.get("/events")
def search_events(filters: EventFilters = Depends(), session: Session = Depends(get_session)):
    where = ["starts_at >= CURRENT_DATE"]
    if filters.q:
        where.append(f"title ILIKE '%{filters.q}%'")
    if filters.venue:
        where.append(f"venue = '{filters.venue}'")
    sql = f"SELECT id, title, venue, starts_at FROM events WHERE {' AND '.join(where)} LIMIT {filters.limit}"
    return [dict(r) for r in session.execute(text(sql)).mappings()]
