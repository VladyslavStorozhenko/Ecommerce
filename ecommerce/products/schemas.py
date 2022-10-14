from pydantic import BaseModel, conint, constr


class Category(BaseModel):
    name: constr(min_length=3, max_length=50)


class DisplayCategory(Category):
    id: int

    class Config:
        orm_mode = True


class BaseProduct(BaseModel):
    name: constr(min_length=3, max_length=50)
    description: constr(min_length=5, max_length=200)
    quantity: conint(ge=0, le=99)
    price: float


class Product(BaseProduct):
    category_id: int


class DisplayProduct(BaseProduct):
    id: int
    category: DisplayCategory

    class Config:
        orm_mode = True
