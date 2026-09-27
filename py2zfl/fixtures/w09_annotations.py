from uuid import UUID
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

@app.get("/o/{order_id}", response_class=HTMLResponse)
def order(order_id: UUID, note: str):
    open(f"/orders/{order_id}.pdf")                    # clean: a UUID
    return f"<p>{note}</p>"                            # EXPECT: REFUTED (a declared-HTML body)
