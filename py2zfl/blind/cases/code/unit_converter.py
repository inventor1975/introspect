from enum import Enum

from fastapi import FastAPI

app = FastAPI()


class Operation(str, Enum):
    add = "+"
    sub = "-"
    mul = "*"
    div = "/"


@app.get("/convert/{op}")
def apply_op(op: Operation, a: float, b: float = 1.0):
    expression = f"{a!r} {op.value} {b!r}"
    return {"expression": expression, "result": eval(expression)}
