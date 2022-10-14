import pytest
from faker import Faker
from ..conf_test_db import override_get_db
from ecommerce.products import crud as products_crud, schemas as products_schemas, models as products_models


@pytest.fixture
def dummy_product_out_of_stock(dummy_category: products_models.Category, faker: Faker) -> products_models.Product:
    data = {'name': 'Iphone 1',
            'description': faker.text(200),
            'quantity': 0,
            'price': float(faker.random_number()),
            'category_id': dummy_category.id}
    database = next(override_get_db())
    created_product_data = products_crud.create_product(products_schemas.Product(**data), database)
    yield created_product_data

    products_crud.delete_product(created_product_data.id, database)
