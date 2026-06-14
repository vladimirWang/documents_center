from fastapi import APIRouter, Depends, Security
from fastapi.security import SecurityScopes

from deps.verify_token import verify_token
from module_user.user_vo import user_login, user_register
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
def login(user: user_login):
    token = create_access_token({"user_id": 1, "username": user.username})
    return {"token": token}


@user_router.post("/add_user")
def add_user(user: user_register):
    return {"success": True, "data": user.model_dump()}
