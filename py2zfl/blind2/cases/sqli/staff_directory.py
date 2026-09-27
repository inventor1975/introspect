from fastapi import FastAPI
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, select

engine = create_engine("postgresql+psycopg2://hr@localhost/hr")
metadata = MetaData()
staff = Table(
    "staff",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("department", String),
)
app = FastAPI()


@app.get("/staff")
def staff_directory(department: str, name_prefix: str = ""):
    stmt = select(staff.c.id, staff.c.name).where(staff.c.department == department)
    if name_prefix:
        stmt = stmt.where(staff.c.name.startswith(name_prefix))
    with engine.connect() as conn:
        rows = conn.execute(stmt.order_by(staff.c.name)).all()
    return [{"id": r.id, "name": r.name} for r in rows]
