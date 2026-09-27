from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class QuoteRequest(BaseModel):
    customer_id: int
    base_amount: float = Field(gt=0)
    formula: str = "base_amount * 1.2"


@app.post("/quotes")
def create_quote(body: QuoteRequest):
    ns = {"base_amount": body.base_amount}
    exec(f"total = {body.formula}", ns)
    return {"customer_id": body.customer_id, "total": ns["total"]}
