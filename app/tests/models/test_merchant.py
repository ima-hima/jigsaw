import pytest
import psycopg2

from .context import backend
from backend.src.models import City, CityZipcode, Merchant, Zipcode
from backend.src.db import drop_all_tables
from backend.src.orm import find_or_create


@pytest.fixture()
def city():
    drop_all_tables()

    brooklyn = find_or_create(City(name='Brooklyn'))[0]
    manhattan = find_or_create(City(name='Manhattan'))[0]
    philadelphia = find_or_create(City(name='Philadelphia'))[0]

    south_philly_zip = find_or_create(Zipcode(name=19019))[0]
    chelsea_zip = find_or_create(Zipcode(name=10001))[0]
    gramercy_zip = find_or_create(Zipcode(name=10010))[0]
    dumbo_zip = find_or_create(Zipcode(name=11210))[0]
    zips_list = ['11221', '11231', '11220', '11201', '11210']
    brooklyn_zips = [find_or_create(Zipcode(name=z))[0] for z in zips_list]

    for zipcode in brooklyn_zips:
        find_or_create(CityZipcode(city_id=brooklyn.id, zip_id=zipcode.id))[0]
    yield city
    drop_all_tables()

def test_city_multiple_zipcodes(city):
    pass
    # codes = [zipcode.name for zipcode in city.zipcodes(cursor)]
    # assert codes == [10001, 10010]


def test_city(city):
    city = City()


# def test_city_zipcode(city):
#     city = City()
