from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine("sqlite:///events.db")
SessionLocal = sessionmaker(bind=engine)
app = FastAPI()


class Registration(BaseModel):
    event_code: str
    email: str
    seats: int = 1


def get_session():
    with SessionLocal() as session:
        yield session


@app.post("/registrations", status_code=201)
def register(reg: Registration, db: Session = Depends(get_session)):
    stmt = text(
        "INSERT INTO registrations (event_code, email, seats) VALUES ('{}', :email, :seats)".format(
            reg.event_code
        )
    )
    db.execute(stmt, {"email": reg.email, "seats": reg.seats})
    db.commit()
    return {"status": "registered"}
