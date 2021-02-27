import psycopg2
import os

from backend.src.db import conn, cursor, retrieve_record, retrieve_records
import backend.settings as settings

TABLES = ['areacodes', 
          'zipcodes', 
          'cities', 
          'merchants', 
          'areacodes_zipcodes', 
          'cities_zipcodes'
         ]

def build_from_record(This_class, record):
    """
    Given a record returned from the DB, build an object of 
    class This_class with attributes based on that record.
    """
    if not record: 
        return None
    attr = dict(zip(This_class.columns, record))
    obj = This_class()
    obj.__dict__ = attr
    return obj

def build_from_records(This_class, records):
    """
    Given records returned from the DB, build a list of 
    objects of This_class with attributes based on that record.
    """
    return [build_from_record(This_class, record) for record in records]

def clear_db():
    pass

def find_all(This_class):
    records = retrieve_records(This_class.__table__)
    return [build_from_record(This_class, record) for record in records]

def find_by_id(This_class, input_id):
    """
    Retrieve record by id from DB, create and return obj of type This_class
    with values from that record.
    """
    record = retrieve_record(This_class.__table__, 'id', input_id)
    return build_from_record(This_class, record)

def find_by_name(This_class, name):
    """
    Retrieve record by name from DB, create and return obj of type This_class
    with values from that record.
    """
    record = retrieve_record(This_class.__table__, 'name', name)
    return build_from_record(This_class, record)

def find_or_create(obj):
    """
    Save values in input obj into DB. Return a *list* of *new* 
    objects of same type.
    """
    values_str = ', '.join(len(values(obj)) * ['%s'])
    keys_str = ', '.join(keys(obj))
    insert_str = f'INSERT INTO {obj.__table__} ({keys_str}) VALUES ({values_str});'
    try:
        cursor.execute(insert_str, list(values(obj)))
        conn.commit()
        cursor.execute(f'SELECT * FROM {obj.__table__} ORDER BY id DESC LIMIT 1')
    except Exception as e: # Need to have exception for unique fields. 
                           # Must do SELECT after insertion. 
                           # Doing SELECT first would return values already 
                           # inserted for non-unique fields.
        condition_str = ' WHERE '
        for k in keys(obj):
            condition_str += k + ' = %s AND '
        condition_str = condition_str[:-5]
        cursor.execute('ROLLBACK')
        cursor.execute('SELECT * FROM ' + obj.__table__ + condition_str, tuple(values(obj)))
    records = cursor.fetchall() # fetchall() and not fetchone() in case of 
                                # non-unique fields
    result = build_from_records(type(obj), records)
    return result

def values(obj):
    """Return a list of values from the __dict__ in obj."""
    obj_attrs = obj.__dict__
    return [obj_attrs[attr] for attr in obj.columns if attr in obj_attrs.keys()]

def keys(obj):
    """Return a list of values from the __dict__ in obj."""
    obj_attrs = obj.__dict__
    return [attr for attr in obj.columns if attr in obj_attrs.keys()]

