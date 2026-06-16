from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database.models import Product
from database.session import get_db


def get_db_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product
