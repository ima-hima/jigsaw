import psycopg2
import pytest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../')))

import api

import api.src.db as db
# import api.src.models as models
import api.src.adapters as adapters

from first_input import reports


def fill_db():
    builder = adapters.Builder()
    for report in reports:
        builder.run(report, db.conn, db.cursor)


fill_db()

print("finished filling")
