from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from common.resp import BaseResp
from database.session import get_db
from module_client.client_service import register_client
from module_client.client_vo import ClientCreate

client_router = APIRouter(
    prefix="/client",
    tags=["客户端管理"],
)


@client_router.get("/")
def client_list(db: Session = Depends(get_db)):
    return BaseResp.success(data={"clients": []})


@client_router.post("/", status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    try:
        db_client = register_client(
            db,
            email=client.email,
            password=client.password,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return BaseResp.success(
        data={
            "id": db_client.id,
            "email": db_client.email,
            "mobile": db_client.mobile,
            "created_at": db_client.created_at,
            "updated_at": db_client.updated_at,
        },
        msg="注册成功",
    )