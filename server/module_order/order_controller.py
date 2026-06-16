from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.session import get_db
from module_order.order_vo import OrderCreate
from module_order.order_service import create_order_data, get_order_by_id, get_order_list, serialize_order
from common.resp import BaseResp

order_router = APIRouter(
    prefix="/order",
    tags=["订单"],
)

@order_router.get("/")
def order_list(db: Session = Depends(get_db)):
    orders = get_order_list(db)
    return BaseResp.success(data={"orders": [serialize_order(order) for order in orders]})


@order_router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = create_order_data(order, db)
    # return BaseResp.success(data={"order": 123})
    return BaseResp.success(data={"order": serialize_order(new_order)})


@order_router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = get_order_by_id(order_id, db)
    return BaseResp.success(data={"order": serialize_order(order)})