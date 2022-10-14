from ..conf_test_db import client
from fastapi import status
from ecommerce.cart.models import CartItems
from faker import Faker


def test_create_order(user_item: CartItems, auth_token: str, faker: Faker):
    response = client.post('/orders/', json={'shipping_address': faker.address()},
                           headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_201_CREATED
    order_data = response.json()
    assert len(order_data['order_details']) == 1
    assert order_data['order_price'] == user_item.quantity * user_item.product.price

    client.delete(f'/orders/{order_data["id"]}', headers={'Authorization': f'Bearer {auth_token}'})


def test_create_order_no_items(auth_token: str, faker: Faker):
    response = client.post('/orders/', json={'shipping_address': faker.address()},
                           headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'There are no items in cart'}


def test_get_orders(user_item: CartItems, auth_token: str, faker: Faker):
    client.post('/orders/', json={'shipping_address': faker.address()},
                headers={'Authorization': f'Bearer {auth_token}'})
    response = client.get('/orders/all', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_200_OK
    order_data = response.json()
    assert len(order_data) == 1
    assert order_data[0]['order_details'][0]['quantity'] == user_item.quantity

    client.delete(f'/orders/{order_data[0]["id"]}', headers={'Authorization': f'Bearer {auth_token}'})


def test_delete_order(user_item: CartItems, auth_token: str, faker: Faker):
    created_order = client.post('/orders/', json={'shipping_address': faker.address()},
                                headers={'Authorization': f'Bearer {auth_token}'})
    response = client.delete(f'/orders/{created_order.json()["id"]}',
                             headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    order_response = client.get('/orders/all', headers={'Authorization': f'Bearer {auth_token}'})
    assert order_response.status_code == status.HTTP_200_OK
    order_data = order_response.json()
    assert len(order_data) == 0
