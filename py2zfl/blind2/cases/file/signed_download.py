import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from werkzeug.utils import secure_filename

app = FastAPI()

RELEASES = "/srv/releases"


@app.get("/releases/download")
async def download_release(request: Request):
    requested = request.query_params.get("artifact", "")
    display_name = secure_filename(requested)
    if not display_name:
        raise HTTPException(status_code=400, detail="bad artifact name")
    candidate = os.path.join(RELEASES, requested)
    if not os.path.isfile(candidate):
        raise HTTPException(status_code=404, detail=f"{display_name} not found")
    return FileResponse(candidate, filename=display_name)
