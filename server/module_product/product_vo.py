from pydantic import BaseModel, Field
from typing import Annotated

ProductNameStr = Annotated[str, Field(min_length=1, max_length=30)]
ProductDescriptionStr = Annotated[str, Field(default="", max_length=255)]
ProductPriceFloat = Annotated[float, Field(gt=0)]

class ProductCreate(BaseModel):
    name: ProductNameStr
    description: ProductDescriptionStr
    price: ProductPriceFloat

class ProductUpdate(BaseModel):
    name: ProductNameStr
    description: ProductDescriptionStr
    price: ProductPriceFloat

class ProductDelete(BaseModel):
    id: int