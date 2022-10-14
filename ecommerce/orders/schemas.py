from pydantic import BaseModel, constr
from datetime import datetime
from ..user.schemas import DisplayUser
from ..products.schemas import DisplayProduct


class OrderDetails(BaseModel):
    order_id: int
    product_id: int


class DisplayOrderDetails(BaseModel):
    id: int
    quantity: int
    product: DisplayProduct

    class Config:
        orm_mode = True


class Order(BaseModel):
    shipping_address: constr(min_length=3, max_length=200)


class DisplayOrder(Order):
    id: int
    created_date: datetime
    order_price: float
    order_status: str
    user_id: int
    user: DisplayUser
    order_details: list[DisplayOrderDetails] = []

    class Config:
        orm_mode = True

