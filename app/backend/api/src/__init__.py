from distutils import util
from flask import Flask, request
import simplejson as json
import os

from api.src.models import Areacode, City, CityZipcode, Merchant, Table, Zipcode
from api.src.orm import find_all, find_by_id
import settings as settings
# from .adaptors import *


TESTING = settings.TEST
DEBUGGING = settings.DEBUG


def create_app(database='jigsaw_project_test', testing = settings.TEST, debug = settings.DEBUG):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(DATABASE = database, DEBUG = settings.DEBUG, TESTING = settings.TEST)

    @app.route('/')
    def root_url():
        return 'Welcome to my api.'

    @app.route('/cities')
    def cities():
        """Return complete records for all cities in DB."""
        cities = orm.find_all(models.City)
        city_names = [city.__dict__ for city in cities]
        return json.dumps(city_names, default=str)

    @app.route('/cities/areacodes/<city_id>')
    def areacodes_for_city(city_id):
        """
        For a city given by city_id, return complete record for all
        areacodes in that city.
        """
        areacodes = orm.find_by_id(City, city_id).areacodes()
        areacode_names = [areacode.__dict__ for zipcode in areacodes]
        return json.dumps(areacode_names, default = str)

    @app.route('/cities/<city_id>')
    def city(city_id):
        """Return complete record for city with id == city_id."""
        city = orm.find_by_id(models.City, city_id)
        return json.dumps(city.__dict__, default=str)

    @app.route('/cities/merchants/<city_id>')
    def merchants_for_city(city_id):
        """ For a city with name city_id, return all merchants in that city."""
        merchants = orm.find_by_id(City, city_id).merchants()
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/cities/zipcodes/<city_id>')
    def zips_for_city(city_id):
        """
        For a city given by city_id, return complete record for all
        zipcodes in that city.
        """
        zipcodes = orm.find_by_id(City, city_id).zipcodes()
        print(zipcodes)
        zipcode_names = [zipcode.__dict__ for zipcode in zipcodes]
        return json.dumps(zipcode_names, default = str)

    @app.route('/zipcodes')
    def zipcodes():
        """Return all zipcodes in DB."""
        zipcodes = orm.find_all(models.Zipcode)
        zipcode_dicts = [zipcode.__dict__ for zipcode in zipcodes]
        return json.dumps(zipcode_dicts, default=str)

    @app.route('/zipcodes/areacodes/<zip_id>')
    def areacodes_for_zip(zip_id):
        """
        For a zipcode given by zip_id, return complete record for all
        areacodes in that zipcode.
        """
        areacodes = orm.find_by_id(Zipcode, zip_id).areacodes()
        areacode_names = [areacode.__dict__ for zipcode in areacodes]
        return json.dumps(areacode_names, default = str)

    @app.route('/zipcodes/cities/<zip_id>')
    def cities_for_zip(zip_id):
        """ For a zip with id == zip_id, return all cities in that zipcode."""
        cities = orm.find_by_id(Zipcode, zip_id).cities()
        city_dicts = [city.__dict__ for city in cities]
        return json.dumps(city_dicts, default=str)

    @app.route('/zipcodes/merchants/<zip_id>')
    def merchants_for_zip(zip_id):
        """ For a zip with id zip_id, return all merchants in that zipcode."""
        merchants = orm.find_by_id(Zipcode, zip_id).merchants()
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/merchants')
    def merchants():
        """Return all merchants in DB."""
        merchants = orm.find_all(models.Merchant)
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/merchants/<merchant_id>')
    def merchant(merchant_id):
        """Return complete record for merchant with id == merchant_id."""
        merchant = orm.find_by_id(models.City, merchant_id)
        return json.dumps(merchant.__dict__, default=str)

    @app.route('/merchants/city/zip/<merchant_id>')
    def zip_and_city_of_merchant(merchant_id):
        """ For a merchant with name merchant_id, return its zipcode and city."""
        merchant = orm.find_by_id(Merchant, merchant_id)
        zipcode = merchant.zipcode()
        city = merchant.city()
        merchant_dicts = [{'zipcode': zipcode.name, 'city': city.name}]
        return json.dumps(merchant_dicts, default=str)

    return app


