import pytest

from .context import api
from api.src.models import City, Receipt
from api.src.db import drop_all_tables
from api.src.orm import find_or_create


@pytest.fixture
def set_up_tear_down_db():
    drop_all_tables()
    yield
    drop_all_tables()


def test_receipt(set_up_tear_down_db):
    first = find_or_create(Receipt(name='Brooklyn'))[0]
    # manhattan = find_or_create(City(name='Manhattan'))
    # philadelphia = find_or_create(City(name='Philadelphia'))
