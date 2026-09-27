import psycopg2
from fastapi import FastAPI

app = FastAPI()
DSN = "dbname=warehouse user=wms"


@app.get("/bins/{zone}")
def bins_in_zone(zone: str, aisle: str = "A"):
    conn = psycopg2.connect(DSN)
    try:
        cur = conn.cursor()
        cur.execute(
            query=f"SELECT code, capacity, used FROM bins WHERE zone = '{zone}' AND aisle = '{aisle}'"
        )
        return [{"code": c, "capacity": cap, "used": u} for c, cap, u in cur.fetchall()]
    finally:
        conn.close()
