from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from . import crud, schemas
from ..auth.services import get_current_user
from ..cart.crud import get_cart_by_user_id
from ..db import get_db
from ..user.schemas import DisplayUser

router = APIRouter(tags=['Orders'], prefix='/orders')


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.DisplayOrder)
def create_order(order: schemas.Order, current_user: DisplayUser = Depends(get_current_user),
                 database: Session = Depends(get_db)):
    user_cart = get_cart_by_user_id(current_user.id, database)
    if not user_cart or not user_cart.cart_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='There are no items in cart')

    order = crud.create_order_with_details(order, user_cart, database)
    return order


@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[schemas.DisplayOrder])
def get_user_orders(current_user: DisplayUser = Depends(get_current_user), database: Session = Depends(get_db)):
    return crud.get_user_orders(current_user.id, database)


@router.delete('/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, current_user: DisplayUser = Depends(get_current_user),
                 database: Session = Depends(get_db)):
    crud.delete_order(order_id, database)
