import psycopg2
import pytest
from decimal import *
import api.src.db.db as db
import api.src.models as models
import api.src.adapters as adapters
# from tests.adapters.venue_details import imperfect_venue_details


def insert_data():
    test_cursor = test_conn.cursor()
    builder = adapters.Builder()
    venue_objs = builder.run(venue_details, test_conn, test_cursor)
    venue = venue_objs['venue']
    location = venue_objs['location']
    venue_categories = venue_objs['venue_categories']
    zipcode = location.zipcode(test_cursor)
    city = zipcode.city(test_cursor)
    state = city.state(test_cursor)
    
def test_when_exists_finds_existing_venue_location_and_categories(test_conn):
    test_cursor = test_conn.cursor()
    builder = adapters.Builder()
    venue_objs = builder.run(venue_details, test_conn, test_cursor)
    venue = venue_objs['venue']
    location = venue_objs['location']
    venue_categories = venue_objs['venue_categories']
    zipcode = location.zipcode(test_cursor)
    city = zipcode.city(test_cursor)
    state = city.state(test_cursor)

    new_venue_objs = builder.run(venue_details, test_conn, test_cursor)
    new_venue = new_venue_objs['venue']
    new_location = new_venue_objs['location']
    new_venue_categories = new_venue_objs['venue_categories']
    new_zipcode = location.zipcode(test_cursor)
    new_city = new_zipcode.city(test_cursor)
    new_state = new_city.state(test_cursor)

    assert venue.id == new_venue.id
    assert location.id == new_location.id
    assert city.id == new_city.id
    assert state.id == new_state.id
    assert zipcode.id == new_zipcode.id
    assert location.id == new_location.id
    assert  venue_categories[0].id == new_venue_categories[0].id


def test_when_imperfect_data_exists_builds_new_venue_location_and_categories(test_conn):
    test_cursor = test_conn.cursor()
    builder = adapters.Builder()
    venue_objs = builder.run(imperfect_venue_details, test_conn, test_cursor)
    venue = venue_objs['venue']
    location = venue_objs['location']
    venue_categories = venue_objs['venue_categories']
    zipcode = location.zipcode(test_cursor)
    city = zipcode.city(test_cursor)
    state = city.state(test_cursor)

    assert venue.name == 'Country Boys Tacos'
    assert venue.foursquare_id == '53aefe43498ec970f3cf4aea'
    assert location.latitude == Decimal('40.699322354013994')
    assert location.longitude == Decimal('-73.97475273514199')
    assert zipcode.code == None
    assert city.name == 'Brooklyn'
    assert state.name == 'NY'
    assert venue_categories[0].category(test_cursor).name == 'Food Truck'
