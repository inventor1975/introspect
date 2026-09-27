import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI(title="config browser")

CONFIG_ROOT = "/etc/myservice/conf.d"


@app.get("/config/{file_path:path}", response_class=PlainTextResponse)
def read_config(file_path: str):
    location = os.path.join(CONFIG_ROOT, file_path)
    try:
        with open(location, "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="missing")
    except IsADirectoryError:
        return "\n".join(sorted(os.listdir(location)))
