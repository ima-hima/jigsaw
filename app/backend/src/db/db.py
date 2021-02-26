from flask import current_app, g
import psycopg2
import os
from dotenv import load_dotenv
from distutils.util import strtobool

load_dotenv()

db_name = os.environ.get('DB_NAME')
if strtobool(os.environ.get('TESTING')):
    db_name += '_test'
db_user = os.environ.get('DB_USER')
db_pw = os.environ.get('DB_PASS')
# TODO: see line 26. Could/should do this in fixture instead, for eventual Flask testing.
# ^^^ huh? line 26? ^^^

TABLES = ['areacodes',
          'zipcodes',
          'cities',
          'merchants',
          'areacodes_zipcodes',
          'cities_zipcodes',
         ]

conn = psycopg2.connect(database=db_name, user=db_user, password=db_pw)
cursor = conn.cursor()

def get_db(database_name=''):
    if "db" not in g:
        g.db = psycopg2.connect(user=db_user, password=db_pw,
            dbname = current_app.config['DATABASE'])
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def drop_records(table_name):
    """Drop all records from table_name."""
    cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()

def drop_tables(table_names):
    """Drop tables in input list table_names."""
    for table_name in table_names:
        drop_records(table_name)

def drop_all_tables():
    """Drop all tables in the database."""
    table_names = TABLES
    drop_tables(table_names)
