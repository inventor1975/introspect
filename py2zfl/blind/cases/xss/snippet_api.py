import html

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/snippet", response_class=HTMLResponse)
async def snippet(text: str = Query("", max_length=2000), lang: str = "text"):
    body = html.escape(text)
    return HTMLResponse(
        content=f'<pre class="lang-{html.escape(lang)}"><code>{body}</code></pre>'
    )
