from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

DATA_ROOT = Path("/srv/opendata/published").resolve()


@app.get("/datasets/{relative_path:path}")
def dataset_file(relative_path: str):
    target = (DATA_ROOT / relative_path).resolve()
    if not target.is_relative_to(DATA_ROOT):
        raise HTTPException(status_code=403, detail="forbidden")
    if not target.is_file():
        raise HTTPException(status_code=404, detail="not found")
    return FileResponse(target)
