# Local libraries
from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.age_model import age_model, age_model_to_dataset, age_model_to_record
from p2f_pydantic.age_model import Age_Model
from service import shared_execution

# Third Party Libraries
from sqlalchemy import insert, select, delete
from sqlalchemy.orm import Session

# Batteries included libraries
import uuid
from typing import List, Optional
from inspect import stack

def list_age_models(output_format: shared_execution.mimes = "application/json",) -> List[Age_Model]:
    logger.debug(f"{fa.service}{fa.list} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(age_model)
        results = shared_execution.list(stmt=stmt,
                                        pydantic_object=Age_Model,
                                        session_object=session,
                                        output_format="application/json")
    return results

def get_age_model(age_model_id: Optional[uuid.UUID]=None,
                  pk_age_model: Optional[int]=None,
                  output_format: shared_execution.mimes = "application/json",) -> Age_Model:
    logger.debug(f"{fa.service}{fa.get} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(age_model)
        if age_model_id is not None:
            stmt = stmt.where(age_model.age_model_id == age_model_id)
        if pk_age_model is not None:
            stmt = stmt.where(age_model.pk_age_model == pk_age_model)
        result = shared_execution.get(stmt=stmt,
                                      pydantic_object=Age_Model,
                                      session_object=session,
                                      output_format="application/json")
    return result

def create_age_model(new_age_model: Age_Model,
                     output_format: shared_execution.mimes = "application/json",) -> Age_Model:
    logger.debug(f"{fa.service}{fa.create} {stack()[0][3]}()")
    if Age_Model.age_model_id == None:
        Age_Model.age_model_id = uuid.uuid4()
    with Session(engine) as session:
        stmt = insert(age_model)
        stmt = stmt.values(
            age_model_name = new_age_model.age_model_name,
            age_model_description = new_age_model.age_model_description,
        )
        pk = shared_execution.create(stmt=stmt,
                                     session_object=session)
    return get_age_model(pk_age_model=pk,
                         output_format=output_format)

def delete_age_model(age_model_id: uuid.UUID,
                     output_format: shared_execution.mimes = "application/json",) -> None:
    logger.debug(f"{fa.service}{fa.delete} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(age_model)
        stmt = stmt.where(age_model.age_model_id == age_model_id)
        shared_execution.delete(stmt=stmt,
                                session_object=session)

def assign_age_model_to_dataset(age_model_id: uuid.UUID, 
                                dataset_id: uuid.UUID,) -> None:
    logger.debug(f"{fa.service}{fa.assign} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(age_model_to_dataset)
        stmt = stmt.values(
            fk_age_model_id = age_model_id,
            fk_dataset_id = dataset_id
        )
        session.execute(stmt)
        session.commit()

def remove_age_model_to_dataset(age_model_id: uuid.UUID, 
                                dataset_id: uuid.UUID) -> None:
    logger.debug(f"{fa.service}{fa.remove} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(age_model_to_dataset)
        stmt = stmt.where(age_model_to_dataset.fk_age_model_id == age_model_id)
        stmt = stmt.where(age_model_to_dataset.fk_dataset_id == dataset_id)
        session.execute(stmt)
        session.commit()

def assign_age_model_to_record(age_model_id: uuid.UUID, 
                                record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.assign} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(age_model_to_record)
        stmt = stmt.values(
            fk_age_model_id = age_model_id,
            fk_record_hash = record_hash
        )
        session.execute(stmt)
        session.commit()

def remove_age_model_to_record(age_model_id: uuid.UUID, 
                                record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.remove} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(age_model_to_record)
        stmt = stmt.where(age_model_to_record.fk_age_model_id == age_model_id)
        stmt = stmt.where(age_model_to_record.fk_record_hash == record_hash)
        session.execute(stmt)
        session.commit()