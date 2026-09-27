from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

app = FastAPI()
LOG_DIR = Path("/var/log/worker")


@app.get("/admin/logs/tail")
def tail_log(name: str = Query(..., min_length=1), lines: int = Query(100, le=2000)):
    log_path = LOG_DIR / name
    if not log_path.exists():
        raise HTTPException(status_code=404, detail="log not found")
    content = log_path.read_text(errors="replace").splitlines()
    return {"name": name, "lines": content[-lines:]}
