from pydantic import BaseModel, Field
from typing import Annotated

OrderQuantityInt = Annotated[int, Field(gt=0, description="数量")]
OrderPriceFloat = Annotated[float, Field(gt=0, description="下单单价")]
OrderRemarkStr = Annotated[str, Field(default="", max_length=255, description="备注")]
ProductIdInt = Annotated[int, Field(gt=0, description="产品ID")]

class OrderItemCreate(BaseModel):
    product_id: ProductIdInt
    quantity: OrderQuantityInt
    price: OrderPriceFloat

class OrderCreate(BaseModel):
    items: Annotated[list[OrderItemCreate], Field(min_length=1, description="订单明细")]
    remark: OrderRemarkStr