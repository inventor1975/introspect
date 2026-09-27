from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from jinja2 import Environment

app = FastAPI()
env = Environment(autoescape=False)

REPORT = env.from_string(
    "<h1>Report: {{ name }}</h1><p>Period: {{ period }}</p><table>{{ rows }}</table>"
)


@app.get("/reports/view")
def view_report(name: str = Query("weekly"), period: str = Query("2026-W39")):
    rows = "<tr><td>visits</td><td>1204</td></tr>"
    return HTMLResponse(REPORT.render(name=name, period=period, rows=rows))
