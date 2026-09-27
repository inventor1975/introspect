from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/items/{item_id}", response_class=HTMLResponse)
def item_page(item_id: int, qty: int = 1):
    total = item_id * qty
    return f"<h1>Item #{item_id}</h1><p>Quantity {qty}, reference total {total}</p>"
