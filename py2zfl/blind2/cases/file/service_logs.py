from collections import deque
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

SERVICE_LOGS = {
    "api": Path("/var/log/platform/api.log"),
    "worker": Path("/var/log/platform/worker.log"),
    "scheduler": Path("/var/log/platform/scheduler.log"),
}


@app.get("/ops/logs")
def service_log(service: str, lines: int = Query(100, ge=1, le=5000)):
    log_path = SERVICE_LOGS.get(service)
    if log_path is None:
        raise HTTPException(status_code=404, detail=f"no log for {service}")
    with log_path.open("r", errors="replace") as fh:
        tail = deque(fh, maxlen=lines)
    return {"service": service, "lines": list(tail)}
