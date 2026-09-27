from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/preview", response_class=HTMLResponse)
async def preview(text: str = Query("", max_length=2000)):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    html = "".join(f"<p>{p}</p>" for p in paragraphs)
    return HTMLResponse(content=f"<article>{html}</article>")
