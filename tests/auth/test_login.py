from ..conf_test_db import client
from ecommerce.user.models import User
from fastapi import status


def test_login(jame_user: User):
    response = client.post('/login', data={'username': jame_user.email, 'password': 'jame123'})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_login_inexistent_user():
    response = client.post('/login', data={'username': 'wrongemail@example.com', 'password': 'wrong_password'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_login_wrong_password(jame_user: User):
    response = client.post('/login', data={'username': jame_user.email, 'password': 'jame12'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}
