# Batteries included libraries
from typing import List, Optional
from uuid import UUID
from inspect import stack

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update

# Local libraries
from p2f_api.apilogs import logger, fa
from service import shared_execution
from ..data.db_connection import engine
from ..data.harm_age import harm_rec_age
from ..data.harm_data_record import harm_data_record
from p2f_pydantic.harm_age import HARM_Rec_Age


def list_harm_ages(
    recent_year_search: Optional[int] = None, 
    older_year_search: Optional[int] = None,
    dataset_id: Optional[UUID] = None,
    output_format: shared_execution.mimes = "application/json",
) -> List[HARM_Rec_Age]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_rec_age)
        if recent_year_search is not None:
            stmt = stmt.where(harm_rec_age.age_mean >= recent_year_search)
        if older_year_search is not None:
            stmt = stmt.where(harm_rec_age.age_mean <= older_year_search)
        if dataset_id is not None:
            dataset_to_rec_subqry = select(harm_data_record.record_hash).distinct()
            dataset_to_rec_subqry = dataset_to_rec_subqry.where(harm_data_record.fk_dataset == dataset_id)
            stmt = stmt.where(harm_rec_age.fk_record_hash.in_(dataset_to_rec_subqry))
        results = shared_execution.list(stmt=stmt,
                                        pydantic_object=HARM_Rec_Age,
                                        session_object=session,
                                        output_format=output_format)
    return results


def get_harm_age(
    record_hash: Optional[str] = None, 
    pk_age: Optional[int] = None,
    output_format: shared_execution.mimes = "application/json",
) -> HARM_Rec_Age:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_rec_age)
        if record_hash is not None:
            stmt = stmt.where(harm_rec_age.fk_record_hash == record_hash)
        if pk_age is not None:
            stmt = stmt.where(harm_rec_age.pk_harm_age == pk_age)
        result = shared_execution.get(stmt=stmt,
                                      pydantic_object=HARM_Rec_Age,
                                      session_object=session,
                                      output_format=output_format)
    return result


def create_new_harm_data_age(new_harm_age: HARM_Rec_Age,
                             output_format: shared_execution.mimes = "application/json",) -> HARM_Rec_Age:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(harm_rec_age)
        stmt = stmt.values(**new_harm_age.model_dump(exclude_unset=True))
        pk = shared_execution.create(stmt=stmt, session_object=session)
    return get_harm_age(pk_age=pk,
                        output_format=output_format)


def update_age(update_harm_age: HARM_Rec_Age,
               output_format: shared_execution.mimes = "application/json",) -> HARM_Rec_Age:
    logger.debug(f"{fa.service}{fa.update} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = update(harm_rec_age)
        stmt = stmt.where(
            harm_rec_age.fk_record_hash == update_harm_age.fk_record_hash
        )
        stmt = stmt.values(**update_harm_age)
        execute = session.execute(stmt)
        commit = session.commit(stmt)
    return get_harm_age(record_hash=update_harm_age.fk_record_hash)


def delete_age(record_hash: str,
               output_format: shared_execution.mimes = "application/json",) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_rec_age)
        stmt = stmt.where(harm_rec_age.fk_record_hash == record_hash)
        shared_execution.delete(stmt=stmt,
                                session_object=session)
