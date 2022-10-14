from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import timedelta
from . import schemas, services
from ..db import get_db

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(tags=['Authentication'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post('/login', response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_db)):
    user = services.authenticate_user(email=form.username, password=form.password, database=database)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password',
                            headers={'WWW_Authenticate': 'Bearer'})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)

    return {'access_token': access_token, 'token_type': 'bearer'}
