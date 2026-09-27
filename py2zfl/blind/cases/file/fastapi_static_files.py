import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()
ASSET_DIR = os.environ.get("ASSET_DIR", "/srv/assets")


@app.get("/assets/{file_path:path}")
async def serve_asset(file_path: str):
    candidate = os.path.join(ASSET_DIR, file_path)
    if not os.path.isfile(candidate):
        raise HTTPException(status_code=404, detail="asset not found")
    return FileResponse(candidate)
