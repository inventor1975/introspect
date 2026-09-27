import html
from enum import Enum

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


class SortOrder(str, Enum):
    newest = "newest"
    oldest = "oldest"
    popular = "popular"


@app.get("/listings")
def listings(q: str = "", order: SortOrder = SortOrder.newest):
    heading = f"<h2>Listings matching {html.escape(q)}</h2>"
    return HTMLResponse(heading + f"<p class='order-{order.value}'>Sorted: {order.value}</p>")
