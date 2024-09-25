from operator import attrgetter

import pytest
from returns.maybe import Nothing
from returns.result import Success, Failure
from operator import eq
from repository.database import create_tables, drop_tables
from model import Store
from repository.store_repo import insert_store, find_store_by_id, delete_store, update_store
import toolz as t


@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    yield
    drop_tables()


@pytest.fixture(scope="module")
def setup_database_with_store(setup_database):
    store = Store(name='metach',
                  state='sar atabaot',
                  city="123456789",
                  street="poiuy")
    yield insert_store(store)


def test_store_creation(setup_database_with_store):
    assert (setup_database_with_store
            .map(attrgetter("id"))
            .map(t.partial(eq, 1))
            .value_or(False))


def test_find_store_by_id(setup_database_with_store):
    assert (find_store_by_id(1)
            .map(attrgetter("id"))
            .map(t.partial(eq, 1))
            .value_or(False))


def test_update_store(setup_database_with_store):
    assert setup_database_with_store is not Nothing
    user = setup_database_with_store.unwrap()
    assert (update_store(1, Store(name='moviestor',
                                  state='unyted kingdem',
                                  city="london",
                                  street="mebakshay hshem"))
            .map(attrgetter("name"))
            .map(lambda name: name != user.name)
            .value_or(False))


def test_delete_store(setup_database_with_store):
    assert isinstance(delete_store(1), Success)
    assert find_store_by_id(1) is Nothing
