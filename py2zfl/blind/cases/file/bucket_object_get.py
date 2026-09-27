import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()
BUCKETS_ROOT = "/srv/object-store"


@app.get("/objects")
def get_object(ref: str):
    try:
        bucket, key = ref.split(":", 1)
    except ValueError:
        raise HTTPException(status_code=400, detail="expected bucket:key")
    object_path = os.path.join(BUCKETS_ROOT, bucket, key)
    if not os.path.isfile(object_path):
        raise HTTPException(status_code=404)
    return FileResponse(object_path)
