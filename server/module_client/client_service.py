from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Client


def get_client_by_email(db: Session, email: str) -> Client | None:
    stmt = select(Client).where(Client.email == email)
    return db.scalar(stmt)


def register_client(db: Session, email: str, password: str) -> Client:
    if get_client_by_email(db, email) is not None:
        raise ValueError("邮箱已存在")

    db_client = Client(email=email, mobile="", password=password)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
