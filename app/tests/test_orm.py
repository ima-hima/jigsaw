import pytest
from decimal import *

from .context import api
from api.src.models import City, Merchant, Zipcode
from api.src.db import drop_all_tables, conn, cursor, find_or_create

@pytest.fixture()
def build_cities():
    db.drop_all_tables(test_conn, db.cursor)
    city = City()
    city.name = 'Brooklyn'
    db.find_or_create(city, test_conn, db.cursor)

    city = City()
    city.name = 'Manhattan'
    db.find_or_create(city, test_conn, db.cursor)
    yield

    db.drop_all_tables(test_conn, db.cursor)

def test_find_all(build_cities):
    pass
    # categories = find_all(city, test_cursor)
    # assert [city.name for city in cities] == ['Brooklyn', 'Manhattan']
