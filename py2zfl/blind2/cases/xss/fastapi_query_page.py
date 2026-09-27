import html

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

DIRECTORY = {"alice": "Room 101", "bob": "Room 214"}


@app.get("/whereis")
async def whereis(q: str = ""):
    room = DIRECTORY.get(q.lower())
    shown = html.escape(q)
    if room is None:
        return HTMLResponse(content=f"<p>No entry for <b>{shown}</b></p>", status_code=404)
    return HTMLResponse(content=f"<p>{shown} sits in {room}</p>")
