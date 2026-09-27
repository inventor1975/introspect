from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text

app = FastAPI()
engine = create_engine("sqlite:///orders.db")


class NoteIn(BaseModel):
    order_id: int
    author: str
    body: str


@app.post("/orders/notes", status_code=201)
def add_note(note: NoteIn):
    if not note.body.strip():
        raise HTTPException(status_code=422, detail="empty note")
    stmt = (
        "INSERT INTO order_notes (order_id, author, body) "
        f"VALUES ({note.order_id}, '{note.author}', '{note.body}')"
    )
    with engine.begin() as conn:
        conn.execute(text(stmt))
    return {"ok": True}
