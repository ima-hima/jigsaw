import psycopg2
import pytest
import os

from .context import backend
from backend.src.db import conn, cursor, drop_records, drop_tables, drop_all_tables
from backend.src.models import Areacode, City, CityZipcode, Merchant, Zipcode

os.environ['TESTING'] = 'True'

# TODO: build out this test suite: it doesn't have enough coverage.
@pytest.fixture
def set_up_tear_down_db():
    drop_all_tables()
    yield
    drop_all_tables()

@pytest.fixture
def insert_records():
    drop_records('areacodes')
    insert_str = 'INSERT INTO areacodes (name) VALUES (%s)'
    for name in ['fir', 'sec', 'thi', 'fou']:
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

def test_drop_records(insert_records):
    """Drop all records from areacodes."""
    query_str = 'SELECT * FROM areacodes'
    cursor.execute(query_str)
    assert cursor.fetchone() is not None
    drop_records('areacodes')
    query_str = 'SELECT * FROM areacodes'
    cursor.execute(query_str)
    assert cursor.fetchone() is None

# def test_drop_tables(table_names, cursor, conn):
#     """Drop tables in input list table_names."""
#     for table_name in table_names:
#         drop_records(table_name, cursor, conn)

# def test_drop_all_tables():
#     """Drop all tables in the database."""
#     table_names = TABLES
#     drop_tables(table_names, cursor, conn)
