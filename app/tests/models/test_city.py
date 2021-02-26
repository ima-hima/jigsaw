import pytest
from backend.src.models import City, Merchant, Zipcode, CityZipcode
from backend.src.orm import drop_all_tables, find_or_create


# @pytest.fixture()
@pytest.fixture
def set_up_tear_down_db():
    drop_all_tables()
    yield
    drop_all_tables(conn, cursor)

def test_city(set_up_tear_down_db):
    brooklyn = find_or_create(City(name='Brooklyn'), conn, cursor)[0]
    # manhattan = find_or_create(City(name='Manhattan'), conn, cursor)
    # philadelphia = find_or_create(City(name='Philadelphia'), conn, cursor)

    south_philly_zip = find_or_create(Zipcode(name=19019), conn, cursor)[0]
    chelsea_zip = find_or_create(Zipcode(name=10001), conn, cursor)[0]
    gramercy_zip = find_or_create(Zipcode(name=10010), conn, cursor)[0]
    dumbo_zip = find_or_create(Zipcode(name=11210), conn, cursor)[0]
    zips_list = ['11221', '11231', '11220', '11201', '11210']
    brooklyn_zips = [find_or_create(Zipcode(name=z), conn, cursor)[0] for z in zips_list]
    for zipcode in brooklyn_zips:
        find_or_create(CityZipcode(city_id=brooklyn.id, zip_id=zipcode.id), conn, cursor)
