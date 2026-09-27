from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from jinja2 import Environment, select_autoescape

app = FastAPI()
env = Environment(autoescape=select_autoescape(default_for_string=True, default=True))

DIGEST = env.from_string(
    "<h1>Digest: {{ name }}</h1><p>Period: {{ period }}</p><ul>{% for i in items %}<li>{{ i }}</li>{% endfor %}</ul>"
)


@app.get("/digest")
def digest(name: str = Query("daily"), period: str = Query("today")):
    items = [f"{name} summary", "No incidents"]
    return HTMLResponse(DIGEST.render(name=name, period=period, items=items))
