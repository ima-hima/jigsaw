from distutils import util
from flask import Flask, request
import simplejson as json
import os

from api.src.models import (Areacode, City, CityZipcode, Merchant,
                            Receipt, Table, Zipcode)
from api.src.orm import find_all, find_by_id
import settings as settings
# from .adaptors import *


TESTING = settings.TEST
DEBUGGING = settings.DEBUG


def create_app(database='jigsaw_project_test',
               testing=settings.TEST,
               debug=settings.DEBUG):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(DATABASE=database,
                            DEBUG=settings.DEBUG,
                            TESTING=settings.TEST)

    @app.route('/')
    def root_url():
        return 'Welcome to my api.'

    @app.route('/cities')
    def cities():
        """Return complete records for all cities in DB."""
        cities = orm.find_all(models.City)
        city_names = [city.__dict__ for city in cities]
        return json.dumps(city_names, default=str)

    @app.route('/cities/<city_id>')
    def city(city_id):
        """Return complete record for city with id == city_id."""
        city = orm.find_by_id(models.City, city_id)
        return json.dumps(city.__dict__, default=str)

    @app.route('/cities/merchants/<city_id>')
    def merchants_for_city(city_id):
        """Return all merchants in city city_id."""
        merchants = orm.find_by_id(City, city_id).merchants()
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/cities/zipcodes/<city_id>')
    def zips_for_city(city_id):
        """Return complete record for all zipcodes in city city_id."""
        zipcodes = orm.find_by_id(City, city_id).zipcodes()
        zipcode_names = [zipcode.__dict__ for zipcode in zipcodes]
        return json.dumps(zipcode_names, default = str)

    @app.route('/zipcodes')
    def zipcodes():
        """Return all zipcodes in DB."""
        zipcodes = orm.find_all(models.Zipcode)
        zipcode_dicts = [zipcode.__dict__ for zipcode in zipcodes]
        return json.dumps(zipcode_dicts, default=str)

    @app.route('/zipcodes/merchants/<zip_id>')
    def merchants_for_zip(zip_id):
        """Return all cities in zipcode zip_id."""
        merchants = orm.find_by_id(Zipcode, zip_id).merchants()
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/zipcodes/<zip_id>')
    def zipcode(zip_id):
        """Return all merchants in zipcode zip_id."""
        zipcode = orm.find_by_id(models.Zipcode, zip_id)
        return json.dumps(zipcode.__dict__, default=str)

    @app.route('/merchants')
    def merchants():
        """Return all merchants in DB."""
        merchants = orm.find_all(models.Merchant)
        merchant_dicts = [merchant.__dict__ for merchant in merchants]
        return json.dumps(merchant_dicts, default=str)

    @app.route('/merchants/<merchant_id>')
    def merchant(merchant_id):
        """Return complete record for merchant merchant_id."""
        merchant = orm.find_by_id(models.City, merchant_id)
        return json.dumps(merchant.__dict__, default=str)

    return app


