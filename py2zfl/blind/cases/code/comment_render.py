from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from jinja2 import Environment, select_autoescape

app = FastAPI()
env = Environment(autoescape=select_autoescape(default_for_string=True))

COMMENT_TEMPLATE = env.from_string(
    "<div class='comment'><b>{{ author }}</b><p>{{ body }}</p></div>"
)


@app.post("/comments/preview", response_class=HTMLResponse)
async def preview_comment(author: str = Form(...), body: str = Form(...)):
    return COMMENT_TEMPLATE.render(author=author, body=body)
