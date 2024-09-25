from operator import attrgetter

import pytest
from returns.maybe import Nothing
from returns.result import Success, Failure
from operator import eq
from repository.database import create_tables, drop_tables
from model import Movie
from repository.movie_repo import insert_movie, find_movie_by_id, delete_movie, update_movie
import toolz as t


@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    yield
    drop_tables()


@pytest.fixture(scope="module")
def setup_database_with_movie(setup_database):
    movie = Movie(genre='metach', year=1995, title='sar atabaot')
    yield insert_movie(movie)


def test_movie_creation(setup_database_with_movie):
    assert (setup_database_with_movie
            .map(attrgetter("id"))
            .map(t.partial(eq, 1))
            .value_or(False))


def test_find_movie_by_id(setup_database_with_movie):
    assert (find_movie_by_id(1)
            .map(attrgetter("id"))
            .map(t.partial(eq, 1))
            .value_or(False))


def test_delete_movie(setup_database_with_movie):
    assert isinstance(delete_movie(1), Success)
    assert find_movie_by_id(1) is Nothing


def test_update_movie(setup_database_with_movie):
    assert setup_database_with_movie is not Nothing
    movie = setup_database_with_movie.unwrap()
    assert (update_movie(1, Movie(title="koko", genre="loco", year=1223))
            .map(attrgetter("title"))
            .map(lambda title: title != movie.title)
            .value_or(False))
