from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

DIRECTORY = {"alice": "Room 101", "bob": "Room 214"}


@app.get("/lookup")
async def lookup(q: str = ""):
    room = DIRECTORY.get(q.lower())
    if room is None:
        return HTMLResponse(content=f"<p>No entry for <b>{q}</b></p>", status_code=404)
    return HTMLResponse(content=f"<p>{q.title()} sits in {room}</p>")
