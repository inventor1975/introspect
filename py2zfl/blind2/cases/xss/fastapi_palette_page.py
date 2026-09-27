from enum import Enum

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


class Swatch(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"


@app.get("/palette/{swatch}", response_class=HTMLResponse)
def palette(swatch: Swatch):
    return (
        f"<div class='swatch' style='background:{swatch.value}'>"
        f"<span>{swatch.value.upper()}</span></div>"
    )
