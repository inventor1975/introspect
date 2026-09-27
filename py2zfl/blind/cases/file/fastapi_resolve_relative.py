from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI()
NOTES_ROOT = Path("/srv/notes").resolve()


@app.get("/notes/{note_path:path}", response_class=PlainTextResponse)
def read_note(note_path: str):
    target = (NOTES_ROOT / note_path).resolve()
    if not target.is_relative_to(NOTES_ROOT):
        raise HTTPException(status_code=403, detail="forbidden")
    if not target.is_file():
        raise HTTPException(status_code=404, detail="not found")
    return target.read_text(encoding="utf-8")
