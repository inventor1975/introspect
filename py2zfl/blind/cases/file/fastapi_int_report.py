import json

from fastapi import FastAPI, HTTPException

app = FastAPI()
REPORT_DIR = "/srv/reports/json"


@app.get("/reports/{report_id}")
def read_report(report_id: int, section: str = "summary"):
    try:
        with open(f"{REPORT_DIR}/{report_id}.json", encoding="utf-8") as fh:
            report = json.load(fh)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="report not found")
    return report.get(section, {})
