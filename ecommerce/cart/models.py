from ecommerce.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='cart')

    cart_items = relationship('CartItems', back_populates='cart')


class CartItems(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())

    cart_id = Column(Integer, ForeignKey('carts.id', ondelete='CASCADE'))
    cart = relationship('Cart', back_populates='cart_items')

    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
    product = relationship('Product', back_populates='cart_items')

    quantity = Column(Integer, default=1)
