import os
from enum import Enum

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

LATEST_DIR = "/srv/warehouse/latest"


class ExportFormat(str, Enum):
    csv = "csv"
    json = "json"
    parquet = "parquet"


@app.get("/exports/latest/{fmt}")
def latest_export(fmt: ExportFormat):
    filename = f"inventory.{fmt.value}"
    return FileResponse(os.path.join(LATEST_DIR, filename), filename=filename)
