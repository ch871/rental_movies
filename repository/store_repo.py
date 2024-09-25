from typing import Optional

from returns.maybe import Maybe, Nothing
from sqlalchemy.exc import SQLAlchemyError

from config.base import session_factory
from model import Store
from returns.result import Result, Success, Failure


def insert_store(store: Store):
    with session_factory() as session:
        try:
            session.add(store)
            session.commit()
            session.refresh(store)
            return Success(store)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))


def find_store_by_id(s_id: int) -> Optional[Store]:
    with session_factory() as session:
        return Maybe.from_optional(
            session.query(Store)
            .filter(Store.id == s_id)
            .first()
        )


def delete_store(s_id: int):
    with session_factory() as session:
        try:
            maybe_store = find_store_by_id(s_id)
            if maybe_store is Nothing:
                return Failure("no store with thees id ")
            store_to_delete = session.merge(maybe_store.unwrap())
            session.delete(store_to_delete)
            session.commit()
            return Success(store_to_delete)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))


def update_store(s_id: int, store: Store):
    with session_factory() as session:
        try:
            maybe_store = find_store_by_id(s_id)
            if maybe_store is Nothing:
                return Failure("no store with thees id ")
            store_to_update = session.merge(maybe_store.unwrap())
            store_to_update.name = store.name
            store_to_update.state = store.state
            store_to_update.city = store.city
            store_to_update.street = store.street
            session.commit()
            session.refresh(store_to_update)
            return Success(store_to_update)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))
