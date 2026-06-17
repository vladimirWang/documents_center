from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import Product
from common.resp import BaseResp
from deps.product import get_db_product
from module_product.product_vo import ProductCreate, ProductUpdate
from agent.product_base import ProductBase

product_router = APIRouter(
    prefix="/product",
    tags=["产品管理"],
)


def _serialize_product(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "balance": product.balance,
        "vectorized": product.vectorized,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
    }


@product_router.get("/")
def product_list(db: Session = Depends(get_db)):
    products = db.scalars(select(Product).order_by(Product.updated_at.desc())).all()
    return BaseResp.success(data={"products": [_serialize_product(p) for p in products]})


@product_router.get("/{product_id}")
def product_detail(db_product: Product = Depends(get_db_product)):
    return BaseResp.success(data={"product": _serialize_product(db_product)})


@product_router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        description=product.description or "",
        price=product.price,
        vectorized=False,
        balance=0,
    )
    db.add(new_product)
    try:
        # 刷新拿到产品id, 避免向量化时没有产品id
        db.flush()
        pb = ProductBase()
        msg = pb.add_product(new_product)
        new_product.vectorized = True
        db.commit()
        # db.refresh(new_product)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(f"创建产品失败: {e}"))
    return BaseResp.success(data={"product": _serialize_product(new_product)})


@product_router.put("/{product_id}")
def update_product(
    product: ProductUpdate,
    db: Session = Depends(get_db),
    db_product: Product = Depends(get_db_product),
):
    db_product.name = product.name
    db_product.description = product.description or ""
    db_product.price = product.price
    db.commit()
    db.refresh(db_product)
    return BaseResp.success(data={"product": _serialize_product(db_product)}, msg="产品更新成功")

@product_router.put("/{product_id}/balance")
def update_product_balance(
    balance: int,
    db: Session = Depends(get_db),
    db_product: Product = Depends(get_db_product),
):
    db_product.balance = balance
    db.commit()
    db.refresh(db_product)
    return BaseResp.success(data={"product": _serialize_product(db_product)}, msg="产品库存更新成功")
