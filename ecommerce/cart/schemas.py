from pydantic import BaseModel
from datetime import datetime
from ecommerce.user.schemas import DisplayUser
from ecommerce.products.schemas import DisplayProduct


class CartItem(BaseModel):
    product_id: int
    quantity: int


class DisplayCartItem(BaseModel):
    id: int
    created_date: datetime
    product: DisplayProduct
    quantity: int

    class Config:
        orm_mode = True


class DisplayCart(BaseModel):
    id: int
    created_date: datetime
    user: DisplayUser
    cart_items: list[DisplayCartItem] = []

    class Config:
        orm_mode = True
