from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import SecurityScopes
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from database.models import User
from database.session import get_db
from deps.user import ensure_email_unique
from deps.verify_token import verify_token
from module_user.user_vo import UserLogin, UserRegister
from utils import create_access_token


def print_scopes(security_scopes: SecurityScopes):
    print("scopes: ", security_scopes.scopes)


user_router = APIRouter(
    prefix="/user",
    tags=["用户管理"],
    dependencies=[Security(print_scopes, scopes=["admin"])],
)


@user_router.get("/user_info")
def user_info(user_info: dict = Depends(verify_token)):
    return user_info

    # return {"user_id": 1, "name": "mike"}
    #


@user_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    stmt = select(User).where(and_(User.email == user.email, User.password == user.password))

    db_user = db.scalar(stmt)
    if db_user is None:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    token = create_access_token({"user_id": db_user.id, "username": db_user.username})
    return {"token": token}


@user_router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
    _: None = Depends(ensure_email_unique),
):
    db_user = User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    # db.refresh(db_user)
    return {"success": True, "data": user.model_dump()}
