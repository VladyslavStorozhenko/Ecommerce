from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, crud
from ..auth.services import get_current_user
from ..db import get_db
from ..products.crud import get_product_by_id
from ..user.schemas import DisplayUser

router = APIRouter(tags=['Cart'], prefix='/cart')


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.DisplayCartItem)
def add_item_to_cart(cart_item: schemas.CartItem, current_user: DisplayUser = Depends(get_current_user),
                     database: Session = Depends(get_db)):
    product_info = get_product_by_id(cart_item.product_id, database)
    if not product_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id {cart_item.product_id} does not exist!')

    if product_info.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Product is out of stock!')

    user_cart = crud.get_cart_by_user_id(current_user.id, database)
    if not user_cart:
        user_cart = crud.create_cart(current_user.id, database)

    new_item = crud.create_item(cart_item, user_cart.id, database)
    return new_item


@router.get('/', response_model=schemas.DisplayCart)
def get_cart(current_user: DisplayUser = Depends(get_current_user), database: Session = Depends(get_db)):
    cart = crud.get_cart_by_user_id(current_user.id, database)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Cart not found. Add item to cart to create it')

    return cart


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item_from_cart(item_id: int, current_user: DisplayUser = Depends(get_current_user),
                          database: Session = Depends(get_db)):
    return crud.delete_item(item_id, current_user.id, database)


@router.delete('/empty/{cart_id}', status_code=status.HTTP_204_NO_CONTENT)
def empty_cart(current_user: DisplayUser = Depends(get_current_user), database: Session = Depends(get_db)):
    cart_id = crud.get_cart_by_user_id(current_user.id, database)
    return crud.empty_cart(cart_id.id, database)
