from fastapi import FastAPI, HTTPException, Query

from lib.formulas import evaluate_formula

app = FastAPI()


@app.get("/pricing/preview")
async def preview_price(
    base: float = Query(...),
    qty: int = Query(1, ge=1),
    formula: str = Query("base * qty"),
):
    try:
        total = evaluate_formula(formula, {"base": base, "qty": qty})
    except (SyntaxError, NameError, ZeroDivisionError) as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"total": total}
