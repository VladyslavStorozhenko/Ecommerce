from fastapi import APIRouter, status, Depends, HTTPException
from .schemas import User, DisplayUser
from sqlalchemy.orm import Session
from ecommerce.db import get_db
from . import crud
from ..auth.services import get_current_user

router = APIRouter(tags=['User'], prefix='/users')


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DisplayUser)
def create_user(user: User, database: Session = Depends(get_db)):
    if crud.get_user_by_email(user.email, database):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This email is already registered!')

    response = crud.create_user_in_db(user, database)
    return response


@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[DisplayUser])
def get_all_users(database: Session = Depends(get_db)):
    response = crud.get_all_users(database)
    return response


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=DisplayUser)
def get_user(user_id: int, database: Session = Depends(get_db)):
    user = crud.get_user_by_id(user_id, database)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} does not exist!')

    return user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, current_user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    return crud.delete_user_in_db(user_id, database)
