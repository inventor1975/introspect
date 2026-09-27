from uuid import UUID

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/orders/{order_id}")
async def order_page(order_id: UUID):
    return HTMLResponse(
        f"<h2>Order {order_id}</h2><p>Short code: {order_id.hex[:8]}</p>"
    )
