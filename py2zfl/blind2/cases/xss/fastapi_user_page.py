from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


def _layout(title: str, body: str) -> str:
    return f"<html><head><title>{title}</title></head><body>{body}</body></html>"


@app.get("/u/{username}", response_class=HTMLResponse)
def user_page(username: str):
    return _layout("Profile", f"<h1>@{username}</h1><p>Recent activity</p>")
