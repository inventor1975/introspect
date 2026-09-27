import os
from enum import Enum

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()
EXPORT_DIR = "/srv/exports/latest"


class ExportFormat(str, Enum):
    csv = "csv"
    json = "json"
    parquet = "parquet"


@app.get("/exports/{fmt}")
def download_export(fmt: ExportFormat):
    path = os.path.join(EXPORT_DIR, f"catalog.{fmt.value}")
    return FileResponse(path, filename=f"catalog.{fmt.value}")
