from flask import current_app, g
import psycopg2
from distutils.util import strtobool
from .context import api, settings


conn_string = (f'host={settings.DB_HOST} '
               f'dbname={settings.DB_NAME} '
               f'user={settings.DB_USER} '
               f'password={settings.DB_PASSWORD}'
               )
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
TABLES = ['areacodes',
          'zipcodes',
          'cities',
          'merchants',
          'areacodes_zipcodes',
          'cities_zipcodes',
          ]


def get_db(database_name=''):
    if "db" not in g:
        g.db = psycopg2.connect(user=db_user,
                                password=db_pw,
                                dbname=current_app.config['DATABASE'])
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


def insert_records(table_name, values, keys):
    placehoders = ', '.join(len(values) * ['%s'])
    keys_str = ', '.join(keys)
    insert_str = (f'INSERT INTO {table_name} ({keys_str}) '
                  f'VALUES ({placehoders});'
                  )
    try:
        cursor.execute(insert_str, list(values))
        conn.commit()
        cursor.execute(f'SELECT * FROM {table_name} '
                       'ORDER BY id DESC LIMIT 1')
    except Exception as e:
      # Need to have exception for unique fields.
      # Must do SELECT after insertion.
      # Doing SELECT first would return values
      # already inserted for non-unique fields.
        condition_str = ' WHERE '
        for k in keys:
            condition_str += k + ' = %s AND '
        condition_str = condition_str[:-5]
        cursor.execute('ROLLBACK')
        cursor.execute(f'SELECT * FROM {table_name} {condition_str}',
                       tuple(values))
    records = cursor.fetchall() # fetchall() and not fetchone() in case
                                # of non-unique fields
    return records


def retrieve_record(table_name, which_field, value):
    """
    Find and return all fields in table table_name for *single record*
    where which_field = value.
    """
    sql_str = f"SELECT * FROM {table_name} WHERE {which_field} = %s"
    cursor.execute(sql_str, (value,))
    return cursor.fetchone()


def retrieve_records(table_name):
    """
    Find and return all fields in table table_name.
    """
    sql_str = f"SELECT * FROM {table_name}"
    cursor.execute(sql_str, tuple())
    return cursor.fetchall()
