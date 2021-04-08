import pytest
import os

from .context import api
from api.src.db import conn, cursor, drop_records, drop_tables, \
                       drop_all_tables, retrieve_record, retrieve_records
from api.src.models import Areacode, City, CityZipcode, Merchant, Zipcode

# drop_records
# drop_tables
# drop_all_tables


os.environ['TESTING'] = 'True'


@pytest.fixture
def set_up_tear_down_db():
    drop_all_tables()
    yield
    drop_all_tables()

@pytest.fixture
def insert_false_records():
    drop_records('areacodes')
    insert_str = 'INSERT INTO areacodes (name) VALUES (%s)'
    for name in ['fir', 'sec', 'thi', 'fou']:
        cursor.execute(insert_str, (name,))
        conn.commit()
    yield

# def test_connection():
#     assert conn.status == 1
#     # Now just make sure the cursor exists.
#     assert cursor

#     query_str = 'SELECT current_database()'
#     cursor.execute(query_str)
#     assert 'jigsaw_project_test' == cursor.fetchone()[0]


def test_drop_records(insert_false_records):
    """Drop all records from areacodes."""
    query_str = 'SELECT * FROM areacodes'
    cursor.execute(query_str)
    assert cursor.fetchone() is not None
    drop_records('areacodes')
    query_str = 'SELECT * FROM areacodes'
    cursor.execute(query_str)
    assert cursor.fetchone() is None


def test_retrieve_record():
    pass


def test_retrieve_records():
    pass

# def test_drop_tables(table_names, cursor, conn):
#     """Drop tables in input list table_names."""
#     for table_name in table_names:
#         drop_records(table_name, cursor, conn)

# def test_drop_all_tables():
#     """Drop all tables in the database."""
#     table_names = TABLES
#     drop_tables(table_names, cursor, conn)


def insert_records(table_name, values, keys):
    placehoders = ', '.join(len(values) * ['%s'])
    keys_str = ', '.join(keys)
    insert_str = f'INSERT INTO {table_name} ({keys_str}) VALUES ({placehoders});'
    try:
        cursor.execute(insert_str, list(values))
        conn.commit()
        cursor.execute(f'SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1')
    except Exception as e: # Need to have exception for unique fields.
                           # Must do SELECT after insertion.
                           # Doing SELECT first would return values already
                           # inserted for non-unique fields.
        condition_str = ' WHERE '
        for k in keys:
            condition_str += k + ' = %s AND '
        condition_str = condition_str[:-5]
        cursor.execute('ROLLBACK')
        cursor.execute(f'SELECT * FROM {table_name} {condition_str}', tuple(values))
    records = cursor.fetchall() # fetchall() and not fetchone() in case of
                                # non-unique fields
    return records

