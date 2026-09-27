from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from jinja2 import Environment, select_autoescape

app = FastAPI()
env = Environment(autoescape=select_autoescape(["html"]))

SAMPLE_CONTEXT = {"first_name": "Dana", "order_no": "A-1042", "total": "49.00"}


@app.post("/admin/email-templates/preview", response_class=HTMLResponse)
async def preview_template(template: str = Form(...), locale: str = Form("en")):
    tmpl = env.from_string(template)
    return tmpl.render(locale=locale, **SAMPLE_CONTEXT)
