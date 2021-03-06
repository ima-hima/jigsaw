import pytest
import psycopg2

from .context import api
from api.src.models import City, CityZipcode, Merchant, Zipcode
from api.src.db import drop_all_tables
from api.src.orm import find_or_create


@pytest.fixture()
def city():
    """
    Build a set of Citys, Zipcodes and Merchants in order to test that constructors
    and accessors are working correctly in model.
    """
    drop_all_tables()

    brooklyn = find_or_create(City(name='Brooklyn'))[0]
    manhattan = find_or_create(City(name='Manhattan'))[0]
    philadelphia = find_or_create(City(name='Philadelphia'))[0]

    south_philly_zip = find_or_create(Zipcode(name='19019'))[0]
    chelsea_zip = find_or_create(Zipcode(name='10001'))[0]
    gramercy_zip = find_or_create(Zipcode(name='10010'))[0]
    dumbo_zip = find_or_create(Zipcode(name='11210'))[0]
    zips_list = ['11221', '11231', '11220', '11201', '11210']
    brooklyn_zips = [find_or_create(Zipcode(name=z))[0] for z in zips_list]

    zipcodes = [find_or_create(CityZipcode(city_id=brooklyn.id, zip_id=z.id))[0] for z in brooklyn_zips]
    yield zipcodes # Yields `zipcodes` back, but will get name 'city' in calling function.
    drop_all_tables()

def test_zipcodes(city):
    pass
    # codes = [z.name for z in city]
    # assert codes == ['10001', '10010']


def test_city(city):
    city = City()

