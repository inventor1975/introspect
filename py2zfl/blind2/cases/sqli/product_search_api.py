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


@app.get("/products/search")
def search_products(q: str = Query(..., min_length=2), db: Session = Depends(get_session)):
    stmt = text(
        f"SELECT id, title, price FROM products WHERE title ILIKE '%{q}%' ORDER BY title LIMIT 50"
    )
    rows = db.execute(stmt).mappings().all()
    return {"results": [dict(r) for r in rows]}
