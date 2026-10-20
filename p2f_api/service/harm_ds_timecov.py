# Batteries included libraries
import uuid
from typing import List, Optional
from inspect import stack

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update

from p2f_api.apilogs import logger, fa
from service import shared_execution
from ..data.db_connection import engine
from ..data.harm_ds_time import harm_ds_timecoverage
from p2f_pydantic.harm_ds_time import HARM_DS_TimeCoverage

# Get
def get_ds_timecov(dataset_id: uuid.UUID,
                   output_format: shared_execution.mimes = "application/json",) -> HARM_DS_TimeCoverage:
    logger.debug(f"{fa.service}{fa.get} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_ds_timecoverage)
        stmt = stmt.where(harm_ds_timecoverage.dataset_id == dataset_id)
        result = shared_execution.get(stmt=stmt,
                                      pydantic_object=HARM_DS_TimeCoverage,
                                      session_object=session,
                                      output_format=output_format)
    return result

# Create
def create_ds_timecov(new_timecov: HARM_DS_TimeCoverage,
                      output_format: shared_execution.mimes = "application/json",) -> HARM_DS_TimeCoverage:
    logger.debug(f"{fa.service}{fa.create} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(harm_ds_timecoverage)
        stmt = stmt.values(
            **new_timecov.model_dump(exclude_unset=True)
        )
        pk = shared_execution.create(stmt=stmt,
                                     session_object=session)
    return get_ds_timecov(dataset_id=new_timecov.dataset_id,
                          output_format=output_format)

# Delete
def delete_ds_timecov(dataset_id: uuid.UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_ds_timecoverage)
        stmt = stmt.where(harm_ds_timecoverage.dataset_id == dataset_id)
        shared_execution.delete(stmt=stmt,
                                session_object=session)
        