import pytest

# from .context import api
from api.src.models import City, Merchant, Receipt
from api.src.db import drop_all_tables
from api.src.orm import find_or_create


@pytest.fixture
def set_up_tear_down():
    drop_all_tables()
    merchant = find_or_create(Merchant(name='Chucks'))[0]
    yield merchant
    drop_all_tables()


def test_receipt(set_up_tear_down):
    print(type(set_up_tear_down))
    merchant_id = set_up_tear_down.id
    first = find_or_create(Receipt(merchant_id=merchant_id))[0]
