from operator import attrgetter

import pytest
from returns.maybe import Nothing
from returns.result import Success, Failure
from operator import eq
from repository.database import create_tables, drop_tables
from model import Rental, Store, Movie, User
from repository.rental_repo import insert_rental, find_rental_by_id, delete_rental, update_rental
from repository.user_repo import insert_user
from repository.movie_repo import insert_movie
from repository.store_repo import insert_store
import toolz as t


@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    yield
    drop_tables()


@pytest.fixture(scope="module")
def setup_database_with_rental(setup_database):
    store = Store(name='metach',
                  state='sar atabaot',
                  city="123456789",
                  street="poiuy")
    user = User(name='metach', email='sar atabaot', phone="123456789")
    movie = Movie(genre='metach', year=1995, title='sar atabaot')
    insert_movie(movie)
    insert_store(store)
    insert_user(user)
    rental = Rental(rental_date="2019-12-04",
                    return_date='2019-12-12',
                    rental_fee=6.0,
                    late_fee=5.8,
                    user_id=1,
                    movie_id=1,
                    store_id=1,
                    )
    yield insert_rental(rental)


def test_rental_creation(setup_database_with_rental):
    assert (setup_database_with_rental
            .map(attrgetter("id"))
            .map(t.partial(eq, 1))
            .value_or(False))


def test_find_rental_by_id(setup_database_with_rental):
    assert (find_rental_by_id(1)
            .map(attrgetter("id"))
            .map(t.partial(eq, 1))
            .value_or(False))


def test_update_rental(setup_database_with_rental):
    assert setup_database_with_rental is not Nothing
    rental = setup_database_with_rental.unwrap()
    assert (update_rental(1, Rental(rental_date="2019-12-04",
                                    return_date='2019-12-12',
                                    rental_fee=6.0,
                                    late_fee=50.8,
                                    user_id=1,
                                    movie_id=1,
                                    store_id=1,
                                    ))
            .map(attrgetter("late_fee"))
            .map(lambda late_fee: late_fee != rental.late_fee)
            .value_or(False))


def test_delete_rental(setup_database_with_rental):
    assert isinstance(delete_rental(1), Success)
    assert find_rental_by_id(1) is Nothing
