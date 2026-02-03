# Local libraries
from p2f_api.apilogs import logger, fa
from ..service.harm_numerical import list_numerics
from ..service.harm_data_record import list_harm_data_record
from ..data.db_connection import engine
from ..data.harm_data_types import harm_data_type
from p2f_pydantic.harm_data_types import harm_data_type as Harm_data_type
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Optional
from uuid import UUID

def list_harm_data_types_by_dataset_id(dataset_id: Optional[UUID]=None) -> List[UUID]:
    logger.debug(f"{fa.service}{fa.get} {__name__} list_harm_data_types_by_dataset_id()")
    data_records = list_harm_data_record(dataset=dataset_id) 
    logger.debug(data_records)
    numeric_records = []
    for data_record in data_records:
        listed_numerics = list_numerics(record_hash=data_record)
        if listed_numerics.data_harmonized_int is not None:
            for record in listed_numerics.data_harmonized_int:
                numeric_records.append(record)
        if listed_numerics.data_harmonized_int_confidence is not None:
            for record in listed_numerics.data_harmonized_int_confidence:
                numeric_records.append(record)
        if listed_numerics.data_harmonized_float is not None:
            for record in listed_numerics.data_harmonized_float:
                numeric_records.append(record)
        if listed_numerics.data_harmonized_float_confidence is not None:
            for record in listed_numerics.data_harmonized_float_confidence:
                numeric_records.append(record)
    numeric_records = {x.fk_data_type for x in numeric_records} # yes this is a set
    return numeric_records

def list_harm_data_types(
        measure: Optional[str]=None, 
        unit_of_measure: Optional[str]=None,
        method: Optional[str]=None,
        dataset_id: Optional[UUID]=None
    ) -> List[Harm_data_type]:
    logger.debug(f"{fa.service}{fa.get} {__name__} {__name__}")
    with Session(engine) as session:
        stmt = select(harm_data_type)
        if measure is not None:
            stmt = stmt.where(harm_data_type.measure == measure)
        if unit_of_measure is not None:
            stmt = stmt.where(harm_data_type.unit_of_measurement == unit_of_measure)
        if method is not None:
            stmt = stmt.where(harm_data_type.method == method)
        results = session.execute(stmt).all()
    results = [Harm_data_type(**x[0].__dict__) for x in results]
    if dataset_id is not None:
        logger.debug("dataset_id is not None")
        dataset_datatypes = list_harm_data_types_by_dataset_id()
        logger.debug(dataset_datatypes)
        results = [x for x in results if x.datatype_id in dataset_datatypes]
    logger.debug(results)
    return results

def get_harm_data_type(
        datatype_id: Optional[UUID]=None,
        pk_harm_data_type: Optional[int]=None
    ) -> Harm_data_type:
    logger.debug(f"{fa.service}{fa.get} {__name__} get_harm_data_type()")
    with Session(engine) as session:
        stmt = select(harm_data_type)
        if datatype_id is not None:
            stmt = stmt.where(harm_data_type.datatype_id == datatype_id)
        if pk_harm_data_type is not None:
            stmt = stmt.where(harm_data_type.pk_harm_data_type == pk_harm_data_type)
        result = session.execute(stmt).first()
    return Harm_data_type(**result.tuple()[0].__dict__)

def create_harm_data_type(
        new_harm_data_type: Harm_data_type    
    ) -> Harm_data_type:
    logger.debug(f"{fa.service}{fa.create} {__name__} create_harm_data_type()")
    with Session(engine) as session:
        stmt = insert(harm_data_type)
        stmt = stmt.values(**new_harm_data_type.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return get_harm_data_type(pk_harm_data_type=execute.inserted_primary_key[0])

def update_harm_data_type(
        update_harm_data_type: Harm_data_type
    ) -> Harm_data_type:
    logger.debug(f"{fa.service}{fa.update} {__name__} update_harm_data_type()")
    with Session(engine) as session:
        stmt = update(harm_data_type)
        stmt = stmt.where(harm_data_type.datatype_id == update_harm_data_type.datatype_id)
        stmt = stmt.values(update_harm_data_type)
        execute = session.execute(stmt)
        commit = session.commit()
    return get_harm_data_type(datatype_id=update_harm_data_type.datatype_id)

def delete_harm_data_type(
        datatype_id: UUID
    ) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} delete_harm_data_type()")
    with Session(engine) as session:
        stmt = delete(harm_data_type)
        logger.debug(datatype_id)
        stmt = stmt.where(harm_data_type.datatype_id == datatype_id)
        execute = session.execute(stmt)
        commit = session.commit()
    return None