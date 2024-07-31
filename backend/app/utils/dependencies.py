from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
