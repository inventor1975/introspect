from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()
engine = create_engine("postgresql+psycopg2://erp:erp@localhost/erp")


@app.get("/suppliers")
def supplier_search(name: str = "", country: str = "NO"):
    stmt = text(
        "SELECT id, name, country FROM suppliers "
        "WHERE country = :country AND name ILIKE :pattern ORDER BY name"
    ).bindparams(country=country, pattern=f"%{name}%")
    with engine.connect() as conn:
        rows = conn.execute(stmt).mappings().all()
    return [dict(r) for r in rows]
