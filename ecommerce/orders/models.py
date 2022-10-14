from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())
    order_price = Column(Float, default=0.0)
    order_status = Column(String(50), default='PROCESSING')
    shipping_address = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='order')

    order_details = relationship('OrderDetails', back_populates='order')


class OrderDetails(Base):
    __tablename__ = 'order_details'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, default=1)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
    order = relationship('Order', back_populates='order_details')

    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
    product = relationship('Product', back_populates='order_details')
