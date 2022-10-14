from ..conf_test_db import client
from ecommerce.user.models import User
from ecommerce.products.models import Product
from ecommerce.cart.models import Cart, CartItems
from ecommerce.auth.services import create_access_token
from fastapi import status


def test_add_item_to_user_without_cart(auth_token: str, dummy_product: Product):
    response = client.post('/cart/', json={'product_id': dummy_product.id, 'quantity': 1},
                           headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert 'id' in data
    assert data['product']['name'] == dummy_product.name

    cart_response = client.get('/cart/', headers={'Authorization': f'Bearer {auth_token}'})
    assert cart_response.status_code == status.HTTP_200_OK
    cart_data = cart_response.json()
    assert 'id' in cart_data
    assert len(cart_data['cart_items']) == 1
    assert cart_data['cart_items'][0]['id'] == data['id']

    client.delete(f'cart/empty/{cart_data["id"]}', headers={'Authorization': f'Bearer {auth_token}'})


def test_add_item_to_user_with_cart(user_cart: Cart, auth_token: str, dummy_product: Product):
    response = client.post('/cart/', json={'product_id': dummy_product.id, 'quantity': 1},
                           headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert 'id' in data
    assert data['product']['name'] == dummy_product.name

    cart_response = client.get('/cart/', headers={'Authorization': f'Bearer {auth_token}'})
    assert cart_response.status_code == status.HTTP_200_OK
    cart_data = cart_response.json()
    assert 'id' in cart_data
    assert len(cart_data['cart_items']) == 1
    assert cart_data['cart_items'][0]['id'] == data['id']

    client.delete(f'cart/empty/{cart_data["id"]}', headers={'Authorization': f'Bearer {auth_token}'})


def test_add_inexistent_product(auth_token: str):
    wrong_product_id = 10000
    response = client.post('/cart/', json={'product_id': wrong_product_id, 'quantity': 1},
                           headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': f'Product with id {wrong_product_id} does not exist!'}


def test_add_item_quantity_error(auth_token: str, dummy_product_out_of_stock: Product):
    response = client.post('/cart/', json={'product_id': dummy_product_out_of_stock.id, 'quantity': 1},
                           headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Product is out of stock!'}


def test_get_cart(user_cart: Cart, auth_token: str, dummy_product: Product):
    response = client.get(f'/cart/', json={'product_id': dummy_product.id, 'quantity': 1},
                          headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['user']['id'] == user_cart.user_id
    assert 'id' in data


def test_get_inexistent_cart(auth_token: str, dummy_product: Product):
    response = client.get('/cart/', json={'product_id': dummy_product.id, 'quantity': 1},
                          headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Cart not found. Add item to cart to create it'}


def test_delete_item(user_item: CartItems, auth_token: str):
    cart_item_id = user_item.id
    response = client.delete(f'/cart/{cart_item_id}', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    cart_response = client.get(f'/cart/', headers={'Authorization': f'Bearer {auth_token}'})
    assert cart_response.status_code == status.HTTP_200_OK
    assert len(cart_response.json()['cart_items']) == 0


def test_delete_inexistent_item(auth_token: str):
    wrong_item_id = 10000
    response = client.delete(f'/cart/{wrong_item_id}',
                             headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': f'Item with id {wrong_item_id} is not in your cart!'}


def test_empty_cart(dummy_user: User, user_item: CartItems):
    auth_token = create_access_token({'sub': dummy_user.email})
    response = client.delete(f'/cart/empty/{user_item.cart_id}',
                             headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    cart_response = client.get(f'/cart/', headers={'Authorization': f'Bearer {auth_token}'})
    assert cart_response.status_code == status.HTTP_404_NOT_FOUND
    assert cart_response.json() == {'detail': 'Cart not found. Add item to cart to create it'}
