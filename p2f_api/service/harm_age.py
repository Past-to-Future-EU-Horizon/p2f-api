# Local libraries
from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.harm_age import harm_data_age
from p2f_pydantic.harm_age import HARM_Data_Age

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update

# Batteries included libraries
from typing import List, Optional
from uuid import UUID
from inspect import stack


def list_harm_ages(
    recent_year_search: Optional[int] = None, older_year_search: Optional[int] = None
) -> List[HARM_Data_Age]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_data_age)
        if recent_year_search is not None:
            stmt = stmt.where(harm_data_age.age_mean >= recent_year_search)
        if older_year_search is not None:
            stmt = stmt.where(harm_data_age.age_mean <= older_year_search)
        results = session.execute(harm_data_age).all()
    return [HARM_Data_Age(**x[0].__dict__) for x in results]


def get_harm_age(
    record_hash: Optional[str] = None, pk_age: Optional[int] = None
) -> HARM_Data_Age:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_data_age)
        if record_hash is not None:
            stmt = stmt.where(harm_data_age.fk_record_hash == record_hash)
        if pk_age is not None:
            stmt = stmt.where(harm_data_age.pk_harm_age == pk_age)
        result = session.execute(stmt)
    return HARM_Data_Age(**result.tuple()[0].__dict__)


def create_new_harm_data_age(new_harm_age: HARM_Data_Age) -> HARM_Data_Age:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(harm_data_age)
        stmt = stmt.values(**new_harm_age)
        execute = session.execute(stmt)
        commit = session.commit()
    return get_harm_age(pk_age=commit.inserted_primary_key[0])


def update_age(update_harm_age: HARM_Data_Age) -> HARM_Data_Age:
    logger.debug(f"{fa.service}{fa.update} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = update(harm_data_age)
        stmt = stmt.where(
            harm_data_age.fk_record_hash == update_harm_age.fk_record_hash
        )
        stmt = stmt.values(**update_harm_age)
        execute = session.execute(stmt)
        commit = session.commit(stmt)
    return get_harm_age(record_hash=update_harm_age.fk_record_hash)


def delete_age(record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_data_age)
        stmt = stmt.where(harm_data_age.fk_record_hash == record_hash)
        execute = session.execute(stmt)
        commit = session.commit()
