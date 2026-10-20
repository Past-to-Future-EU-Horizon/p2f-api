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
# from ..service.harm_numerical import list_numerics
from ..data.db_connection import engine
from ..data.harm_data_record import harm_data_record
from p2f_pydantic.harm_data_record import HARM_Data_Record


def list_harm_data_record(
    dataset: Optional[UUID] = None,
    # data_type: Optional[int]=None,  ## Disabling this for now
    ## I would need to duplicate the code in the numerical service
    ## as this is currently causing circular import issues.
    output_format: shared_execution.mimes = "application/json",
) -> List[HARM_Data_Record]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(harm_data_record)
        if dataset is not None:
            stmt = stmt.where(harm_data_record.fk_dataset == dataset)
        # if data_type is not None: ### Disabled
        #     subqry = (select().subquery())
        results = shared_execution.list(stmt=stmt,
                                        session_object=session, 
                                        pydantic_object=HARM_Data_Record,
                                        output_format=output_format)
    return results


def get_harm_data_record(
    record_hash: Optional[str] = None,
    pk_harm_data_record: Optional[int] = None,
    output_format: shared_execution.mimes = "application/json",
) -> HARM_Data_Record:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(harm_data_record)
        if record_hash is not None:
            stmt = stmt.where(harm_data_record.record_hash == record_hash)
        if pk_harm_data_record is not None:
            stmt = stmt.where(
                harm_data_record.pk_harm_data_record == pk_harm_data_record
            )
        result = shared_execution.get(stmt=stmt,
                                      pydantic_object=HARM_Data_Record,
                                      session_object=session,
                                      output_format=output_format)
    return result

def create_harm_data_record(new_dataset: HARM_Data_Record,
                            output_format: shared_execution.mimes = "application/json",) -> HARM_Data_Record:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = insert(harm_data_record)
        stmt = stmt.values(**new_dataset.model_dump(exclude_unset=True))
        pk = shared_execution.create(stmt=stmt,
                                     session_object=session)
    return get_harm_data_record(pk_harm_data_record=pk,
                                output_format=output_format)


def update_harm_data_record(
    record_hash: str,
    dataset_update: HARM_Data_Record,
    output_format: shared_execution.mimes = "application/json",
) -> HARM_Data_Record:
    logger.debug(f"{fa.service}{fa.update} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = update(harm_data_record)
        stmt = stmt.where(
            harm_data_record.pk_harm_data_record == dataset_update.pk_harm_data_record
        )
        stmt = stmt.values()
        execute = session.execute(stmt)
        commit = session.commit()
    return get_harm_data_record(pk_harm_data_record=dataset_update.pk_harm_data_record)


def delete_harm_data_record(record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = delete(harm_data_record).where(
            harm_data_record.record_hash == record_hash
        )
        shared_execution.delete(stmt=stmt,
                                session_object=session)
    return None
