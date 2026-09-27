from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/feedback", response_class=HTMLResponse)
async def feedback(subject: str = Form(...), message: str = Form("")):
    summary = message[:200]
    return HTMLResponse(
        "<h2>Thanks for your feedback</h2>"
        "<dl><dt>Subject</dt><dd>{}</dd><dt>Message</dt><dd>{}</dd></dl>".format(subject, summary)
    )
