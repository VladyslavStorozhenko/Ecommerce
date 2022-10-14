from sqlalchemy.orm import Session
from . import schemas, models


def create_category(category: schemas.Category, database: Session) -> models.Category:
    new_category = models.Category(**category.dict())
    database.add(new_category)
    database.commit()
    database.refresh(new_category)
    return new_category


def get_all_categories(database: Session) -> list[models.Category]:
    return database.query(models.Category).all()


def get_category_by_name(name: str, database: Session) -> models.Category:
    return database.query(models.Category).filter(models.Category.name == name).first()


def get_category_by_id(category_id: int, database: Session) -> models.Category:
    return database.query(models.Category).filter(models.Category.id == category_id).first()


def delete_category(category_id: int, database: Session):
    database.query(models.Category).filter(models.Category.id == category_id).delete()
    database.commit()


def create_product(product: schemas.Product, database: Session) -> models.Product:
    new_product = models.Product(**product.dict())
    database.add(new_product)
    database.commit()
    database.refresh(new_product)
    return new_product


def get_all_products(database: Session) -> list[models.Product]:
    return database.query(models.Product).all()


def get_product_by_name(name: str, database: Session) -> models.Product:
    return database.query(models.Product).filter(models.Product.name == name).first()


def get_product_by_id(product_id: int, database: Session) -> models.Product:
    return database.query(models.Product).filter(models.Product.id == product_id).first()


def delete_product(product_id: int, database: Session):
    database.query(models.Product).filter(models.Product.id == product_id).delete()
    database.commit()
