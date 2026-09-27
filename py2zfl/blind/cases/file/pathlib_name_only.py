from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()
SUBTITLE_DIR = Path("/srv/media/subtitles")


@app.get("/subtitles")
def subtitles(file: str):
    name = Path(file).name
    if not name.endswith((".vtt", ".srt")):
        raise HTTPException(status_code=400, detail="unsupported subtitle format")
    target = SUBTITLE_DIR / name
    if not target.is_file():
        raise HTTPException(status_code=404)
    return FileResponse(target, media_type="text/vtt")
