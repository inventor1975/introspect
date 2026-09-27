from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/members/{username}")
def member_page(username: str):
    html = f"<html><body><h1>{username}'s page</h1><p>No posts yet.</p></body></html>"
    return HTMLResponse(html)
