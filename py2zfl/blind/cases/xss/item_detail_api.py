from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/items/{item_id}")
def item_detail(item_id: int, qty: int = 1):
    return HTMLResponse(
        f"<h1>Item #{item_id}</h1><p>Quantity in basket: {qty}</p>"
    )
