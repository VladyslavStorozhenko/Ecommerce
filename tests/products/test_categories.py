from tests.conf_test_db import client
from fastapi import status
from ecommerce.products import models


def test_correct_get_category(dummy_category: models.Category):
    response = client.get(f'/products/category/{dummy_category.id}')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert dummy_category.id == data['id']
    assert dummy_category.name == data['name']


def test_incorrect_get_category():
    wrong_category_id = 10000
    response = client.get(f'/products/category/{wrong_category_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': f'Category with id {wrong_category_id} does not exist'}


def test_emtpy_get_all_categories():
    response = client.get('/products/category/all')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_all_categories(dummy_category: models.Category):
    response = client.get('/products/category/all')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == dummy_category.name


def test_delete_category(dummy_category: models.Category):
    response = client.delete(f'/products/category/{dummy_category.id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_category_response = client.get(f'/products/category/{dummy_category.id}')
    assert get_category_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_category_response.json() == {'detail': f'Category with id {dummy_category.id} does not exist'}


def test_create_category():
    category_data = {'name': 'Smartphones'}
    response = client.post('/products/category/', json=category_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['name'] == category_data['name']
    assert 'id' in data
    category_id = data['id']

    response = client.get(f'/products/category/{category_id}')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['name'] == category_data['name']
    assert data['id'] == category_id

    client.delete(f'/products/category/{category_id}')


def test_bad_create_user(dummy_category: models.Category):
    response = client.post('/products/category/', json={'name': dummy_category.name})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': f'Category with name {dummy_category.name} exists'}
