import pytest
from ..conf_test_db import override_get_db
from ecommerce.user import crud as user_crud, schemas as user_schemas, models as user_models


@pytest.fixture
def jame_user() -> user_models.User:
    data = {'name': 'jame',
            'email': 'jame@exapmle.com',
            'password': 'jame123'}
    database = next(override_get_db())
    created_user_data = user_crud.create_user_in_db(user_schemas.User(**data), database)
    yield created_user_data

    user_crud.delete_user_in_db(created_user_data.id, database)
