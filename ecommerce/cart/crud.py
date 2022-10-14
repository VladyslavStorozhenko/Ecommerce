from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas


def create_cart(user_id: int, database: Session) -> models.Cart:
    new_cart = models.Cart(user_id=user_id)
    database.add(new_cart)
    database.commit()
    database.refresh(new_cart)
    return new_cart


def get_cart_by_user_id(user_id: int, database: Session) -> models.Cart:
    return database.query(models.Cart).filter(models.Cart.user_id == user_id).first()


def create_item(cart_item: schemas.CartItem, cart_id: int, database: Session) -> models.CartItems:
    new_item = models.CartItems(cart_id=cart_id, **cart_item.dict())
    database.add(new_item)
    database.commit()
    database.refresh(new_item)
    return new_item


def delete_item(item_id: int, user_id: int, database: Session):
    item_to_delete = database.query(models.CartItems).filter(models.CartItems.id == item_id).first()
    cart_info = get_cart_by_user_id(user_id, database)
    if not cart_info or not item_to_delete or item_to_delete.id not in [item.id for item in cart_info.cart_items]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Item with id {item_id} is not in your cart!')
    database.query(models.CartItems).filter(models.CartItems.id == item_id).delete()
    database.commit()


def empty_cart(cart_id: int, database: Session):
    database.query(models.CartItems).filter(models.CartItems.cart_id == cart_id).delete()
    database.query(models.Cart).filter(models.Cart.id == cart_id).delete()
    database.commit()
