# Local libraries
from p2f_api.apilogs import logger, fa
from ..service.harm_numerical import list_numerics
from ..service.harm_data_record import list_harm_data_record
from ..data.db_connection import engine
from ..data.harm_data_types import harm_data_type
from ..data import harm_data_numerical
from p2f_pydantic.harm_data_types import harm_data_type as Harm_data_type
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from sqlalchemy import text
# Batteries included libraries
from typing import List, Optional
from uuid import UUID
from inspect import stack

def list_harm_data_types_by_dataset_id(dataset_id: Optional[UUID]=None) -> List[UUID]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    data_records = list_harm_data_record(dataset=dataset_id) 
    logger.debug(f"•  data records {data_records}")
    numeric_records = []
    for data_record in data_records:
        logger.debug("•  Iterating through data records")
        listed_numerics = list_numerics(record_hash=data_record.record_hash, 
                                        dataset_id=dataset_id)
        if listed_numerics.data_harmonized_int is not None:
            logger.debug("•• listed_numerics.data_harmonized_int")
            for record in listed_numerics.data_harmonized_int:
                numeric_records.append(record)
        if listed_numerics.data_harmonized_int_confidence is not None:
            logger.debug("•• listed_numerics.data_harmonized_int_confidence")
            for record in listed_numerics.data_harmonized_int_confidence:
                numeric_records.append(record)
        if listed_numerics.data_harmonized_float is not None:
            logger.debug("•• listed_numerics.data_harmonized_float")
            for record in listed_numerics.data_harmonized_float:
                numeric_records.append(record)
        if listed_numerics.data_harmonized_float_confidence is not None:
            logger.debug("•• listed_numerics.data_harmonized_float_confidence")
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
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = select(harm_data_type)
        if measure is not None:
            logger.debug("•• measure is not none")
            stmt = stmt.where(harm_data_type.measure == measure)
        if unit_of_measure is not None:
            logger.debug("•• unit of measure is not none")
            stmt = stmt.where(harm_data_type.unit_of_measurement == unit_of_measure)
        if method is not None:
            logger.debug("•• method is not none")
            stmt = stmt.where(harm_data_type.method == method)
        results = session.execute(stmt).all()
    logger.debug(f"• Found {len(results)} results")
    results = [Harm_data_type(**x[0].__dict__) for x in results]
    if dataset_id is not None:
        logger.debug("•  dataset_id is not None")
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
    return_harm_data_type = get_harm_data_type(pk_harm_data_type=execute.inserted_primary_key[0])
    new_data_type_uuid = return_harm_data_type.datatype_id
    new_data_type_uuid = new_data_type_uuid.hex
    with Session(engine) as session:
        numericals = [harm_data_numerical.harmonized_int,
                      harm_data_numerical.harmonized_int_confidence,
                      harm_data_numerical.harmonized_float,
                      harm_data_numerical.harmonized_float_confidence]
        numericals = [x.__tablename__ for x in numericals]
        for partitioner in numericals:
            stmt = text(f"""CREATE TABLE {partitioner}_{new_data_type_uuid} PARTITION
                        OF {partitioner} FOR VALUES IN ('{new_data_type_uuid}');""")
            session.execute(stmt)
            session.commit()
    return return_harm_data_type

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