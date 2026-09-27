from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text

app = FastAPI()
engine = create_engine("postgresql+psycopg2://inv:inv@localhost/inventory")


@app.get("/inventory/lookup")
def lookup(sku: str = Query(..., min_length=3, max_length=40)):
    with engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT sku, name, qty_on_hand FROM stock WHERE sku = '{sku}'")
        )
        row = result.mappings().first()
    if row is None:
        return {"found": False}
    return {"found": True, "item": dict(row)}
