# Local libraries
from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.harm_timeslice import harm_timeslice, harm_timeslice_to_record
from p2f_pydantic.harm_timeslices import harm_timeslice as Harm_timeslice
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Optional
from uuid import UUID
from inspect import stack

def list_harm_timeslices(
    named_time_period: Optional[str]=None, 
    older_search_age: Optional[int]=None,
    recent_search_age: Optional[int]=None,
    ) -> List[Harm_timeslice]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_timeslice)
        # if named_time_period:
        #     stmt = stmt.where(harm_timeslice.)
        if older_search_age is not None:
            stmt = stmt.where(harm_timeslice.timeslice_age_mean <= older_search_age)
        if recent_search_age is not None:
            stmt = stmt.where(harm_timeslice.timeslice_age_mean >= recent_search_age)
        results = session.execute(stmt).all()
    return [Harm_timeslice(**x[0].__dict__) for x in results]

def get_harm_timeslice(
    timeslice_id: Optional[UUID]=None,
    pk_timeslice: Optional[int]=None,
    ) -> Harm_timeslice:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_timeslice)
        if timeslice_id is not None:
            stmt = stmt.where(harm_timeslice.timeslice_id == timeslice_id)
        if pk_timeslice is not None:
            stmt = stmt.where(harm_timeslice.pk_harm_timeslice == pk_timeslice)
        result = session.execute(stmt)
    return Harm_timeslice(**result.tuple()[0].__dict__)

def create_new_timeslice(
    new_harm_timeslice: Harm_timeslice
    ) -> Harm_timeslice:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(harm_timeslice)
        stmt = stmt.values(**new_harm_timeslice)
        execute = session.execute(stmt)
        commit = session.commit()
    return get_harm_timeslice(pk_timeslice=commit.inserted_primary_key[0])

def update_timeslice(update_harm_timeslice: Harm_timeslice) -> Harm_timeslice:
    logger.debug(f"{fa.service}{fa.update} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = update(harm_timeslice)
        stmt = stmt.where(harm_timeslice.timeslice_id == update_harm_timeslice.timeslice_id)
        stmt = stmt.values(update_harm_timeslice)
        execute = session.execute(stmt)
        commit = session.commit(stmt)
    return get_harm_timeslice(timeslice_id=update_harm_timeslice.timeslice_id)

def delete_timeslice(timeslice_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_timeslice)
        stmt = stmt.where(harm_timeslice.timeslice_id == timeslice_id)
        execute = session.execute(stmt)
        commit = session.commit()

def assign_timeslice(timeslice_id: UUID, 
                     record_hash: str):
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(harm_timeslice_to_record)
        stmt = stmt.values(
            fk_timeslice_id=timeslice_id, 
            fk_record_hash=record_hash
        )
        execute = session.execute(stmt)
        commit = session.commit(stmt)

def remove_timeslice(timeslice_id: UUID, 
                     record_hash: str):
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_timeslice_to_record)
        stmt = stmt.where(harm_timeslice_to_record.fk_timeslice_id == timeslice_id)
        stmt = stmt.where(harm_timeslice_to_record.fk_record_hash == record_hash)
        execute = session.execute(stmt)
        commit = session.commit(stmt)