from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import os

app = FastAPI()

EXPORT_BASE = "/srv/exports"


@app.get("/exports/download")
async def fetch_export(filename: str = Query(..., min_length=1, max_length=200)):
    location = f"{EXPORT_BASE}/{filename}"
    if not os.path.exists(location):
        raise HTTPException(status_code=404, detail="export not found")
    return FileResponse(location, media_type="text/csv")
