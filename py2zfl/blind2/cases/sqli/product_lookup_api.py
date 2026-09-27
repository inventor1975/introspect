from fastapi import Depends, FastAPI, Query
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine("postgresql+psycopg2://catalog@localhost/catalog")
SessionLocal = sessionmaker(bind=engine)
app = FastAPI()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/products/lookup")
def lookup_products(q: str = Query(..., min_length=2), db: Session = Depends(get_session)):
    pattern = f"%{q}%"
    stmt = text(
        "SELECT id, title, price FROM products WHERE title ILIKE :pattern ORDER BY title LIMIT 50"
    )
    rows = db.execute(stmt, {"pattern": pattern}).mappings().all()
    return {"results": [dict(r) for r in rows]}
