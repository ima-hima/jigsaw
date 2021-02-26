from distutils import util
from dotenv import load_dotenv
from flask import Flask, request
import simplejson as json
import os

# from backend.src.db import conn, cursor
from backend.src.models import Areacode, City, CityZipcode, Merchant, Table, Zipcode
from backend.src.orm import find_all, find_by_id

# from .adaptors import *


load_dotenv()

TESTING = bool(util.strtobool(os.environ.get('TESTING')))
DEBUGGING = bool(util.strtobool(os.environ.get('DEBUGGING')))

db_name = os.environ.get('DB_NAME')
if TESTING:
    db_name += '_test'
db_user = os.environ.get('DB_USER')
db_pw = os.environ.get('DB_PASS')

# TODO: What information should I "surface" on, say, city?

def create_app(database='jigsaw_project_test', testing = TESTING, debug = DEBUGGING):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(DATABASE = database, DEBUG = debug, TESTING = testing)

    @app.route('/')
    def root_url():
        return 'Welcome to my api'

    @app.route('/cities')
    def cities():
        """Return complete records for all cities in DB."""
        cities = orm.find_all(models.City, db.cursor)
        city_names = [city.__dict__ for city in cities]
        return json.dumps(city_names, default=str)

    @app.route('/cities/areacodes/<city_id>')
    def areacodes_for_city(city_id):
        """
        For a city given by city_id, return complete record for all
        areacodes in that city.
        """
        areacodes = orm.find_by_id(City, city_id, db.cursor).areacodes(db.cursor)
        areacode_names = [areacode.__dict__ for zipcode in areacodes]
        return json.dumps(areacode_names, default = str)

    @app.route('/cities/<city_id>')
    def city(city_id):
        """Return complete record for city with id == city_id."""
        city = orm.find_by_id(models.City, city_id, db.cursor)
        return json.dumps(city.__dict__, default=str)

    @app.route('/cities/merchants/<city_id>')
    def merchants_for_city(city_id):
        """ For a city with name city_id, return all merchants in that city."""
        merchants = orm.find_by_id(City, city_id, db.cursor).merchants(db.cursor)
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/cities/zipcodes/<city_id>')
    def zips_for_city(city_id):
        """
        For a city given by city_id, return complete record for all
        zipcodes in that city.
        """
        zipcodes = orm.find_by_id(City, city_id, db.cursor).zipcodes(db.cursor)
        print(zipcodes)
        zipcode_names = [zipcode.__dict__ for zipcode in zipcodes]
        return json.dumps(zipcode_names, default = str)

    @app.route('/zipcodes')
    def zipcodes():
        """Return all zipcodes in DB."""
        zipcodes = orm.find_all(models.Zipcode, db.cursor)
        zipcode_dicts = [zipcode.__dict__ for zipcode in zipcodes]
        return json.dumps(zipcode_dicts, default=str)

    @app.route('/zipcodes/areacodes/<zip_id>')
    def areacodes_for_zip(zip_id):
        """
        For a zipcode given by zip_id, return complete record for all
        areacodes in that zipcode.
        """
        areacodes = orm.find_by_id(Zipcode, zip_id, db.cursor).areacodes(db.cursor)
        areacode_names = [areacode.__dict__ for zipcode in areacodes]
        return json.dumps(areacode_names, default = str)

    @app.route('/zipcodes/cities/<zip_id>')
    def cities_for_zip(zip_id):
        """ For a zip with id == zip_id, return all cities in that zipcode."""
        cities = orm.find_by_id(Zipcode, zip_id, db.cursor).cities(db.cursor)
        city_dicts = [city.__dict__ for city in cities]
        return json.dumps(city_dicts, default=str)

    @app.route('/zipcodes/merchants/<zip_id>')
    def merchants_for_zip(zip_id):
        """ For a zip with id zip_id, return all merchants in that zipcode."""
        merchants = orm.find_by_id(Zipcode, zip_id, db.cursor).merchants(db.cursor)
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/merchants')
    def merchants():
        """Return all merchants in DB."""
        merchants = orm.find_all(models.Merchant, db.cursor)
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/merchants/<merchant_id>')
    def merchant(merchant_id):
        """Return complete record for merchant with id == merchant_id."""
        merchant = orm.find_by_id(models.City, merchant_id, db.cursor)
        return json.dumps(merchant.__dict__, default=str)

    @app.route('/merchants/city/zip/<merchant_id>')
    def zip_and_city_of_merchant(merchant_id):
        """ For a merchant with name merchant_id, return its zipcode and city."""
        merchant = orm.find_by_id(Merchant, merchant_id, db.cursor)
        zipcode = merchant.zipcode(db.cursor)
        city = merchant.city(db.cursor)
        merchant_dicts = [{'zipcode': zipcode.name, 'city': city.name}]
        return json.dumps(merchant_dicts, default=str)

    return app


