import psycopg2
import csv
import os
import sys
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../')))
import api

from api.src.models import City, Merchant, Zipcode, CityZipcode
from api.src.db import drop_all_tables, find_or_create, conn, cursor


# import zips and cities
with open('zipcodes.csv') as z:
    zipcodes = csv.DictReader(z, delimiter=',', quotechar='"')
    for zipcode in zipcodes:
        if zipcode['type']:
            new_zip = find_or_create(Zipcode(name=zipcode['zip']),
                                     conn,
                                     cursor)[0]
            new_city = find_or_create(City(name=zipcode['primary_city']),
                                      conn,
                                      cursor)[0]
            cross = find_or_create(CityZipcode(city_id=new_city.id,
                                               zip_id=new_zip.id),
                                   conn,
                                   cursor)[0]
            if zipcode['acceptable_cities']:
                for city in zipcode['acceptable_cities'].split():
                    new_city = find_or_create(City(name=zipcode['acceptable_cities']),
                                              conn,
                                              cursor)[0]
                    cross = find_or_create(CityZipcode(city_id=new_city.id,
                                                       zip_id=new_zip.id),
                                            conn,
                                            cursor)[0]
