import statistics
from typing import List, Literal

from fastapi import FastAPI, Query

app = FastAPI()

FUNCS = {"sum": sum, "max": max, "min": min, "mean": statistics.mean}


@app.get("/stats")
def aggregate(
    agg: Literal["sum", "max", "min", "mean"] = "sum",
    values: List[float] = Query(default=[0.0]),
):
    return {"agg": agg, "value": eval(f"{agg}(values)", dict(FUNCS), {"values": values})}
