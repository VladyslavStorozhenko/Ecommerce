import pytest
from .conf_test_db import override_get_db
from ecommerce.user import crud as user_crud, schemas as user_schemas, models as user_models
from ecommerce.products import crud as products_crud, schemas as products_schemas, models as products_models
from ecommerce.cart import crud as cart_crud, schemas as cart_schemas, models as cart_models
from ecommerce.auth import services
from faker import Faker


@pytest.fixture
def dummy_user(faker: Faker) -> user_models.User:
    data = {'name': faker.name(),
            'email': faker.email(),
            'password': faker.password()}
    database = next(override_get_db())
    created_user_data = user_crud.create_user_in_db(user_schemas.User(**data), database)
    yield created_user_data

    user_crud.delete_user_in_db(created_user_data.id, database)


@pytest.fixture
def user_cart(dummy_user: user_models.User) -> cart_models.Cart:
    database = next(override_get_db())
    created_cart_data = cart_crud.create_cart(dummy_user.id, database)
    yield created_cart_data

    cart_crud.empty_cart(created_cart_data.id, database)


@pytest.fixture
def user_item(user_cart: cart_models.Cart, dummy_product: products_models.Product) -> cart_models.CartItems:
    database = next(override_get_db())
    created_item_data = cart_crud.create_item(cart_schemas.CartItem(product_id=dummy_product.id, quantity=1),
                                              user_cart.id, database)
    yield created_item_data


@pytest.fixture
def auth_token(dummy_user: user_models.User) -> str:
    token = services.create_access_token({'sub': dummy_user.email})
    return token


@pytest.fixture
def dummy_category() -> products_models.Category:
    data = {'name': 'Smartphones'}
    database = next(override_get_db())
    created_category_data = products_crud.create_category(products_schemas.Category(**data), database)
    yield created_category_data

    products_crud.delete_category(created_category_data.id, database)


@pytest.fixture
def dummy_product(dummy_category: products_models.Category, faker: Faker) -> products_models.Product:
    data = {'name': 'Iphone 13',
            'description': faker.text(200),
            'quantity': faker.random_int(1, 99),
            'price': float(faker.random_number()),
            'category_id': dummy_category.id}
    database = next(override_get_db())
    created_product_data = products_crud.create_product(products_schemas.Product(**data), database)
    yield created_product_data

    products_crud.delete_product(created_product_data.id, database)
