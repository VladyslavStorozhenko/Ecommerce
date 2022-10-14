from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session
from ..products.models import Product
from . import models, schemas, tasks
from .. products.crud import get_product_by_id
from ..cart.crud import empty_cart
from ..cart.models import CartItems, Cart


def create_order(order: schemas.Order, user_id: int, database: Session) -> models.Order:
    new_order = models.Order(user_id=user_id, **order.dict())
    database.add(new_order)
    database.commit()
    database.refresh(new_order)
    return new_order


def create_order_with_details(order: schemas.Order, cart: Cart, database: Session) -> models.Order:
    new_order = create_order(order, cart.user_id, database)

    price = 0.0
    for cart_item in cart.cart_items:
        product_info = reduce_product_quantity(cart_item, database)

        price += product_info.price

        order_details = schemas.OrderDetails(order_id=new_order.id, product_id=product_info.id)
        create_order_details(order_details, database)

    new_order.order_price = price
    database.commit()

    # tasks.send_email.delay('fastapi@givmail.com')

    empty_cart(cart.id, database)
    return new_order


def reduce_product_quantity(cart_item: CartItems, database: Session) -> Product:
    product_info = get_product_by_id(cart_item.product_id, database)
    if product_info.quantity >= cart_item.quantity:
        product_info.quantity -= cart_item.quantity
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not enough products in supply!')
    database.commit()
    return product_info


def create_order_details(order_details: schemas.OrderDetails, database: Session):
    order_details_info = database.query(models.OrderDetails).filter(and_(
        models.OrderDetails.order_id == order_details.order_id,
        models.OrderDetails.product_id == order_details.product_id
    )).first()
    if not order_details_info:
        new_order_details = models.OrderDetails(**order_details.dict())
        database.add(new_order_details)
        database.commit()
        database.refresh(new_order_details)
    else:
        order_details_info.quantity += 1
        database.commit()


def get_user_orders(user_id: int, database: Session) -> list[models.Order]:
    return database.query(models.Order).filter(models.Order.user_id == user_id).all()


def delete_order(order_id: int, database: Session):
    database.query(models.Order).filter(models.Order.id == order_id).delete()
    database.commit()
