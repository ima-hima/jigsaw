import pytest
import psycopg2

from .context import api
from api.src.models import Areacode, City, Merchant, Zipcode, CityZipcode
from api.src.db import find_or_create, conn, cursor


@pytest.fixture()
def city():
    drop_all_tables(conn, cursor)

    brooklyn = save(City(name='Brooklyn'), conn, cursor)
    manhattan = save(City(name='Manhattan'), conn, cursor)
    philadelphia = save(City(name='Philadelphia'), conn, cursor)

    south_philly_zip = save(Zipcode(name=19019), conn, cursor)
    chelsea_zip = save(Zipcode(name=10001), conn, cursor)
    gramercy_zip = save(Zipcode(name=10010), conn, cursor)
    dumbo_zip = save(Zipcode(name=11210), conn, cursor)
    zips_list = ['11221', '11231', '11220', '11201', '11210']
    brooklyn_zips = [save(Zipcode(name=z), conn, cursor) for z in zips_list]

    for zipcode in brooklyn_zips:
        save(CityZipcode(city_id=brooklyn.id, zipcode=zipcode.name), conn, cursor)
    yield
    drop_all_tables(conn, cursor)

def test_zipcodes(city):
    codes = [zipcode.name for zipcode in city.zipcodes(cursor)]
    assert codes == [10001, 10010]


def test_city(city):
    city = City()


# def test_city_zipcode(city):
#     city = City()
