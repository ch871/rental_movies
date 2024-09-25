from operator import attrgetter

import pytest
from returns.maybe import Nothing
from returns.result import Success, Failure
from operator import eq
from repository.database import create_tables, drop_tables
from model import User
from repository.user_repo import insert_user, find_user_by_id, delete_user, update_user
import toolz as t


@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    yield
    drop_tables()


@pytest.fixture(scope="module")
def setup_database_with_user(setup_database):
    user = User(name='metach', email='sar atabaot', phone="123456789")
    yield insert_user(user)


def test_user_creation(setup_database_with_user):
    assert (setup_database_with_user
            .map(attrgetter("id"))
            .map(t.partial(eq, 1))
            .value_or(False))


def test_find_user_by_id(setup_database_with_user):
    assert (find_user_by_id(1)
            .map(attrgetter("id"))
            .map(t.partial(eq, 1))
            .value_or(False))


def test_update_user(setup_database_with_user):
    assert setup_database_with_user is not Nothing
    user = setup_database_with_user.unwrap()
    assert (update_user(1, User(name='chaim', email='sar@atabaot', phone="050-6789543"))
            .map(attrgetter("name"))
            .map(lambda name: name != user.name)
            .value_or(False))


def test_delete_user(setup_database_with_user):
    assert isinstance(delete_user(1), Success)
    assert find_user_by_id(1) is Nothing
