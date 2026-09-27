import os
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

BLOB_ROOT = "/srv/blobs"


@app.get("/blobs/{blob_id}")
def fetch_blob(blob_id: str):
    try:
        token = uuid.UUID(blob_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="malformed id")
    location = os.path.join(BLOB_ROOT, token.hex[:2], f"{token}.bin")
    if not os.path.exists(location):
        raise HTTPException(status_code=404)
    return FileResponse(location, media_type="application/octet-stream")
