from fastapi import APIRouter, Depends, status, HTTPException
from . import schemas, crud
from sqlalchemy.orm import Session
from ..db import get_db


router = APIRouter(tags=['Products'], prefix='/products')


@router.post('/category/', status_code=status.HTTP_201_CREATED, response_model=schemas.DisplayCategory)
def create_category(category: schemas.Category, database: Session = Depends(get_db)):
    if crud.get_category_by_name(category.name, database):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Category with name {category.name} exists')

    category = crud.create_category(category, database)
    return category


@router.get('/category/all', status_code=status.HTTP_200_OK, response_model=list[schemas.DisplayCategory])
def get_all_categories(database: Session = Depends(get_db)):
    categories = crud.get_all_categories(database)
    return categories


@router.get('/category/{category_id}', status_code=status.HTTP_200_OK, response_model=schemas.DisplayCategory)
def get_category(category_id: int, database: Session = Depends(get_db)):
    category = crud.get_category_by_id(category_id, database)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Category with id {category_id} does not exist')
    return category


@router.delete('/category/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, database: Session = Depends(get_db)):
    return crud.delete_category(category_id, database)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.DisplayProduct)
def create_product(product: schemas.Product, database: Session = Depends(get_db)):
    if not crud.get_category_by_id(product.category_id, database):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='You provided category id that does not exist')

    new_product = crud.create_product(product, database)
    return new_product


@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[schemas.DisplayProduct])
def get_all_products(database: Session = Depends(get_db)):
    products = crud.get_all_products(database)
    return products


@router.get('/{product_id}', status_code=status.HTTP_200_OK, response_model=schemas.DisplayProduct)
def get_product(product_id: int, database: Session = Depends(get_db)):
    product = crud.get_product_by_id(product_id, database)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id {product_id} does not exist')

    return product


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, database: Session = Depends(get_db)):
    crud.delete_product(product_id, database)
