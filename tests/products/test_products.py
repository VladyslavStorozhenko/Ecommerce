from tests.conf_test_db import client
from fastapi import status
from ecommerce.products import models
from faker import Faker


def test_correct_get_product(dummy_product: models.Product):
    response = client.get(f'/products/{dummy_product.id}')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert dummy_product.id == data['id']
    assert dummy_product.name == data['name']
    assert dummy_product.category_id == data['category']['id']


def test_incorrect_get_product():
    wrong_product_id = 10000
    response = client.get(f'/products/{wrong_product_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': f'Product with id {wrong_product_id} does not exist'}


def test_emtpy_get_all_categories():
    response = client.get('/products/all')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_all_categories(dummy_product: models.Product):
    response = client.get('/products/all')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == dummy_product.name
    assert data[0]['category']['id'] == dummy_product.category_id


def test_delete_product(dummy_product: models.Product):
    response = client.delete(f'/products/{dummy_product.id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_product_response = client.get(f'/products/{dummy_product.id}')
    assert get_product_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_product_response.json() == {'detail': f'Product with id {dummy_product.id} does not exist'}


def test_create_product(dummy_category: models.Category, faker: Faker):
    product_data = {'name': 'Iphone 13',
                    'description': faker.text(200),
                    'quantity': faker.random_int(1, 99),
                    'price': float(faker.random_number()),
                    'category_id': dummy_category.id}
    response = client.post('/products/', json=product_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['name'] == product_data['name']
    assert data['category']['id'] == product_data['category_id']
    assert 'id' in data
    product_id = data['id']

    response = client.get(f'/products/{product_id}')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['name'] == product_data['name']
    assert data['category']['id'] == product_data['category_id']
    assert data['id'] == product_id

    client.delete(f'/products/{product_id}')


def test_bad_create_user(dummy_product: models.Product, faker: Faker):
    data = {'name': 'Iphone 13',
            'description': faker.text(200),
            'quantity': faker.random_int(1, 99),
            'price': float(faker.random_number()),
            'category_id': 10000}
    response = client.post('/products/', json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'You provided category id that does not exist'}
