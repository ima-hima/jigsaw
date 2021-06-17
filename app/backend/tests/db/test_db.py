import pytest

# from .context import api
from api.src.db import (conn, cursor, drop_records, drop_tables,
                        drop_all_tables, retrieve_record, retrieve_records)
from api.src.models import City, CityZipcode, Merchant, Zipcode

# drop_records
# drop_tables
# drop_all_tables

zips_to_insert = ['11122', '11112', '12345', '54321']

@pytest.fixture
def set_up_tear_down_db():
    drop_all_tables()
    yield
    drop_all_tables()

@pytest.fixture
def insert_false_records():
    drop_records('zipcodes')
    insert_str = 'INSERT INTO zipcodes (name) VALUES (%s)'
    for name in zips_to_insert:
        cursor.execute(insert_str, (name,))
        conn.commit()
    yield

def test_connection():
    assert conn.status == 1
    # Now just make sure the cursor exists.
    assert cursor

    query_str = 'SELECT current_database()'
    cursor.execute(query_str)
    assert 'jigsaw_project_test' == cursor.fetchone()[0]


def test_drop_records(insert_false_records):
    """Drop all records from zipcodes."""
    query_str = 'SELECT * FROM zipcodes'
    cursor.execute(query_str)
    assert cursor.fetchone() is not None
    drop_records('zipcodes')
    query_str = 'SELECT * FROM zipcodes'
    cursor.execute(query_str)
    assert cursor.fetchone() is None


def test_retrieve_record(insert_false_records):
    record = retrieve_record('zipcodes', 'name', '11122')
    print(record)
    assert record[1] == '11122'


def test_retrieve_records(insert_false_records):
    records = retrieve_records('zipcodes')
    zips = set(zips_to_insert)
    for zipcode in records:
        assert zipcode[1] in zips



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
        # Doing SELECT first would return values already
        # inserted for non-unique fields.
        condition_str = ' WHERE '
        for k in keys:
            condition_str += k + ' = %s AND '
        condition_str = condition_str[:-5]
        cursor.execute('ROLLBACK')
        cursor.execute(f'SELECT * FROM {table_name} {condition_str}',
                       tuple(values))
    records = cursor.fetchall()
    return records
