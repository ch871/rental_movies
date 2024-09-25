from typing import Optional

from returns.maybe import Maybe, Nothing
from sqlalchemy.exc import SQLAlchemyError

from config.base import session_factory
from model import Movie
from returns.result import Result, Success, Failure


def insert_movie(movie: Movie):
    with session_factory() as session:
        try:
            session.add(movie)
            session.commit()
            session.refresh(movie)
            return Success(movie)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))


def find_movie_by_id(m_id: int) -> Optional[Movie]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.query(Movie)
            .filter(Movie.id == m_id)
            .first()
        )


def delete_movie(m_id: int):
    with session_factory() as session:
        try:
            maybe_movie = find_movie_by_id(m_id)
            if maybe_movie is Nothing:
                return Failure("no movie with thees id ")
            movie_to_delete = session.merge(maybe_movie.unwrap())
            session.delete(movie_to_delete)
            session.commit()
            return Success(movie_to_delete)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))


def update_movie(m_id: int, movie: Movie):
    with session_factory() as session:
        try:
            maybe_movie = find_movie_by_id(m_id)
            if maybe_movie is Nothing:
                return Failure("no movie with thees id ")
            movie_to_update = session.merge(maybe_movie.unwrap())
            movie_to_update.year = movie.year
            movie_to_update.genre = movie.genre
            movie_to_update.title = movie.title
            session.commit()
            session.refresh(movie_to_update)
            return Success(movie_to_update)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))
