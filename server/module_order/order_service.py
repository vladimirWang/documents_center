from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Order, OrderProduct
from module_order.order_vo import OrderCreate


def _serialize_order_item(item: OrderProduct) -> dict:
    return {
        "product_id": item.product_id,
        "quantity": item.quantity,
        "price": item.price,
    }


def serialize_order(order: Order) -> dict:
    return {
        "id": order.id,
        "total_price": order.total_price,
        "remark": order.remark,
        "items": [_serialize_order_item(item) for item in order.items],
        "created_at": order.created_at,
        "updated_at": order.updated_at,
    }


def create_order_data(order: OrderCreate, db: Session) -> Order:
    total_price = sum(item.quantity * item.price for item in order.items)
    new_order = Order(
        total_price=total_price,
        remark=order.remark,
        items=[
            OrderProduct(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
            for item in order.items
        ],
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_order_list(db: Session) -> list[Order]:
    return db.scalars(select(Order).order_by(Order.created_at.desc())).all()


def get_order_by_id(order_id: int, db: Session) -> Order:
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order
