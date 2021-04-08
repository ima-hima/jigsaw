from api.src.db import drop_all_tables, insert_records, \
    retrieve_record, retrieve_records


TABLES = ['areacodes',
          'zipcodes',
          'cities',
          'merchants',
          'receipts',
          'areacodes_zipcodes',
          'cities_zipcodes',
          ]


def build_from_record(cls, record):
    """
    Given a record returned from the DB, build an object of
    class cls with attributes based on that record.
    """
    if not record:
        return None
    attr = dict(zip(cls.columns, record))
    obj = cls()
    obj.__dict__ = attr
    return obj


def build_from_records(cls, records):
    """
    Given records returned from the DB, build a list of
    objects of cls with attributes based on that record.
    """
    return [build_from_record(cls, record) for record in records]


def clear_db():
    drop_all_tables()


def find_all(cls):
    """Get all records for cls and return cls objects."""
    records = retrieve_records(cls.__table__)
    return [build_from_record(cls, record) for record in records]


def find_by_id(cls, input_id):
    """
    Retrieve record by id from DB, create and return obj of type cls
    with values from that record.
    """
    record = retrieve_record(cls.__table__, 'id', input_id)
    return build_from_record(cls, record)


def find_by_name(cls, name):
    """
    Retrieve record by name from DB, create and return obj of type cls
    with values from that record.
    """
    record = retrieve_record(cls.__table__, 'name', name)
    return build_from_record(cls, record)


def find_or_create(obj):
    """
    Save values in input obj into DB. Return a *list* of *new*
    objects of same type.
    """
    records = insert_records(obj.__table__, values(obj), keys(obj))

    result = build_from_records(type(obj), records)
    return result


def values(obj):
    """Return a list of values from the __dict__ in obj."""
    obj_attrs = obj.__dict__
    return [obj_attrs[attr] for attr in obj.columns
            if attr in obj_attrs.keys()]


def keys(obj):
    """Return a list of values from the __dict__ in obj."""
    obj_attrs = obj.__dict__
    return [attr for attr in obj.columns
            if attr in obj_attrs.keys()]
