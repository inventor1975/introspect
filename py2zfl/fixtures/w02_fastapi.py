from typing import Literal
from fastapi import FastAPI, Query
app = FastAPI()

@app.get("/calc")
def calc(expr: str = Query("1+1"), op: Literal["sum", "avg"] = Query("sum")):
    eval(expr)                               # EXPECT: REFUTED (a query parameter)
    eval(op + "(xs)")                        # clean: Literal-validated
