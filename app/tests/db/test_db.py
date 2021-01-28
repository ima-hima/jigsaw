import psycopg2
import pytest

from .context import backend
from backend.src.db import *
from backend.src.models import Areacode, City, CityZipcode, Merchant, Zipcode

# TODO: build out this test suite: it doesn't have enough coverage.

@pytest.fixture
def set_up_tear_down_db():
    drop_all_tables(conn, cursor)
    yield
    drop_all_tables(conn, cursor)

def test_find_or_create_unique(set_up_tear_down_db):
    """Test whether unique condition will work for unique key on one column."""
    record = find_or_create(Zipcode(name='90210'), conn, cursor)[0]
    
    # Zips are unique. We save same value, should return same id.
    record2 = find_or_create(Zipcode(name='90210'), conn, cursor)[0]
    assert record.id == record2.id
    record = find_or_create(City(name='Brooklyn'), conn, cursor)[0]
    
    # City names are not unique. We save same value, should return different id.
    record2 = find_or_create(City(name='Brooklyn'), conn, cursor)[0]
    assert record.id == record2.id

def test_multiple_not_unique(set_up_tear_down_db):
    """Test whether unique condition will work for unique key on two columns."""
    zipcode = find_or_create(Zipcode(name='90210'), conn, cursor)[0]
    # Zips are unique. We save same value, should return same id.
    zipcode2 = find_or_create(Zipcode(name='90210'), conn, cursor)[0]
    assert zipcode.id == zipcode2.id
    merchant = find_or_create(Merchant(name='Sammy\'s'), conn, cursor)[0]
    # Merchant names are not unique. We save same value, should return different id.
    merchant2 = find_or_create(Merchant(name='Sammy\'s'), conn, cursor)[0]
    assert merchant.id != merchant2.id

def test_find_all(set_up_tear_down_db):
    find_or_create(City(name='Brooklyn'), conn, cursor)[0]
    find_or_create(City(name='LA'), conn, cursor)[0]
    cities = find_all(City, cursor)
    assert [city.name for city in cities] == ['Brooklyn', 'LA']


