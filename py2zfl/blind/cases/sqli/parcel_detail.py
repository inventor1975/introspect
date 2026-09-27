import sqlite3

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/parcels/{parcel_id}")
async def parcel_detail(parcel_id: int, include_history: bool = False):
    conn = sqlite3.connect("parcels.db")
    parcel = conn.execute(
        f"SELECT id, sender, recipient, status FROM parcels WHERE id = {parcel_id}"
    ).fetchone()
    if parcel is None:
        raise HTTPException(status_code=404)
    history = []
    if include_history:
        history = conn.execute(
            f"SELECT at, location, event FROM parcel_events WHERE parcel_id = {parcel_id} ORDER BY at"
        ).fetchall()
    conn.close()
    return {"parcel": parcel, "history": history}
