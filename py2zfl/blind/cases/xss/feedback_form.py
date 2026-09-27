from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/feedback")
async def feedback(
    name: str = Form(...),
    rating: int = Form(...),
    remarks: str = Form(""),
):
    stars = "*" * max(0, min(rating, 5))
    body = f"<h2>Thanks, {name}!</h2><p>{stars}</p><blockquote>{remarks}</blockquote>"
    return HTMLResponse(body)
