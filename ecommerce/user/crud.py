from . import models, schemas
from sqlalchemy.orm import Session


def create_user_in_db(user: schemas.User, database: Session) -> models.User:
    new_user = models.User(**user.dict())
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


def get_user_by_email(email: str, database: Session) -> models.User:
    return database.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(user_id: int, database: Session) -> models.User:
    return database.query(models.User).filter(models.User.id == user_id).first()


def get_all_users(database: Session) -> list[models.User]:
    return database.query(models.User).all()


def delete_user_in_db(user_id: int, database: Session):
    database.query(models.User).filter(models.User.id == user_id).delete()
    database.commit()
