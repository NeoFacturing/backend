from sqlalchemy.orm import Session
from app.database.schemas import User


def get_user(db: Session, username: str):
    return db.query(User).filter(User.email == username).first()
