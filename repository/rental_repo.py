from typing import Optional

from returns.maybe import Maybe, Nothing
from sqlalchemy.exc import SQLAlchemyError

from config.base import session_factory
from model import Rental
from returns.result import Result, Success, Failure
from repository.movie_repo import find_movie_by_id
from repository.user_repo import find_user_by_id
from repository.store_repo import find_store_by_id


def insert_rental(rental: Rental):
    with session_factory() as session:
        try:
            maybe_store = find_store_by_id(rental.store_id)
            if maybe_store is Nothing:
                return Failure("no store with thees id ")
            maybe_user = find_user_by_id(rental.user_id)
            if maybe_user is Nothing:
                return Failure("no user with thees id ")
            maybe_movie = find_movie_by_id(rental.movie_id)
            if maybe_movie is Nothing:
                return Failure("no movie with thees id ")
            session.add(rental)
            session.commit()
            session.refresh(rental)
            return Success(rental)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))


def find_rental_by_id(r_id: int) -> Optional[Rental]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.query(Rental)
            .filter(Rental.id == r_id)
            .first()
        )


def delete_rental(r_id: int):
    with session_factory() as session:
        try:
            maybe_rental = find_rental_by_id(r_id)
            if maybe_rental is Nothing:
                return Failure("no rental with thees id ")
            rental_to_delete = session.merge(maybe_rental.unwrap())
            session.delete(rental_to_delete)
            session.commit()
            return Success(rental_to_delete)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))


def update_rental(r_id: int, rental: Rental):
    with session_factory() as session:
        try:
            maybe_rental = find_rental_by_id(r_id)
            if maybe_rental is Nothing:
                return Failure("no rental with thees id ")
            rental_to_update = session.merge(maybe_rental.unwrap())
            rental_to_update.rental_fee = rental.rental_fee
            rental_to_update.late_fee = rental.late_fee
            rental_to_update.rental_date = rental.rental_date
            rental_to_update.return_date = rental.return_date
            rental_to_update.total_payment = rental.total_payment
            rental_to_update.user_id = rental.user_id
            rental_to_update.movie_id = rental.movie_id
            rental_to_update.store_id = rental.store_id
            session.commit()
            session.refresh(rental_to_update)
            return Success(rental_to_update)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))
