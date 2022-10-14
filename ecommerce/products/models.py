from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    product = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(200))
    quantity = Column(Integer)
    price = Column(Float)

    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    category = relationship('Category', back_populates='product')

    cart_items = relationship('CartItems', back_populates='product')

    order_details = relationship('OrderDetails', back_populates='product')
