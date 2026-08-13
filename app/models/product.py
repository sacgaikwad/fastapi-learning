from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float


class ProductRequest(Product):
    pass

class ProductResponse(BaseModel):
    product_id: int
    name: str
    price: float
