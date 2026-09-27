import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

PUBLIC_ROOT = "/var/app/public"


@app.get("/share/{name}")
def shared_file(name: str):
    resolved = os.path.realpath(os.path.join(PUBLIC_ROOT, name))
    if not resolved.startswith(PUBLIC_ROOT):
        raise HTTPException(status_code=403, detail="outside share")
    if not os.path.isfile(resolved):
        raise HTTPException(status_code=404)
    return FileResponse(resolved)
