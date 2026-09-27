from fastapi import FastAPI
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://ledger@localhost/ledger")
app = FastAPI()


@app.get("/ledger/{account}/total")
def ledger_total(account: str, currency: str = "EUR"):
    with engine.connect() as conn:
        total = conn.exec_driver_sql(
            f"SELECT COALESCE(SUM(amount), 0) FROM ledger WHERE account = '{account}' "
            "AND currency = %(cur)s",
            {"cur": currency},
        ).scalar()
    return {"account": account, "currency": currency, "total": float(total)}
