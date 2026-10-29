# Batteries included libraries
from typing import List, Optional
from uuid import UUID, uuid4
from inspect import stack

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from sqlalchemy import union
from sqlalchemy import text

# Local libraries
from p2f_api.apilogs import logger, fa
from service import shared_execution
from ..service.harm_numerical import list_numerics_type_iterator
from ..service.harm_data_record import list_harm_data_record
from ..data.db_connection import engine
from ..data.harm_data_types import harm_data_type, datatype_to_dataset
from ..data.harm_data_numerical import harmonized_float_confidence, harmonized_float
from ..data.harm_data_numerical import harmonized_int_confidence, harmonized_int
from ..data.harm_data_record import harm_data_record
from ..data.harm_locations import harm_location_to_rec
from ..data import harm_data_numerical
from p2f_pydantic.harm_data_types import HARM_Data_Type

def list_harm_data_types(
    measure: Optional[str] = None,
    unit_of_measure: Optional[str] = None,
    method: Optional[str] = None,
    dataset_id: Optional[UUID] = None,
    location_id: Optional[UUID] = None, 
    is_proxy: Optional[bool] = None,
    active_datatypes: Optional[bool] = None,
    output_format: shared_execution.mimes = "application/json"
) -> List[HARM_Data_Type]:
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
        if is_proxy is not None:
            logger.debug("•• is_proxy is not none")
            stmt = stmt.where(harm_data_type.is_proxy == is_proxy)
        if dataset_id is not None:
            logger.debug("•• dataset_id is not none")
            subqry_d = select(harm_data_record.record_hash.distinct()).where(harm_data_record.fk_dataset == dataset_id)
            subqry_i = select(harmonized_int.fk_data_type.distinct()).where(harmonized_int.fk_data_record.in_(subqry_d))
            subqry_ic = select(harmonized_int_confidence.fk_data_type.distinct()).where(harmonized_int_confidence.fk_data_record.in_(subqry_d))
            subqry_f = select(harmonized_float.fk_data_type.distinct()).where(harmonized_float.fk_data_record.in_(subqry_d))
            subqry_fc = select(harmonized_float_confidence.fk_data_type.distinct()).where(harmonized_float_confidence.fk_data_record.in_(subqry_d))
            stmt = stmt.where(harm_data_type.datatype_id.in_(union(subqry_i, subqry_ic, subqry_f, subqry_fc)))
        if location_id is not None:
            logger.debug("•• location_id is not none")
            subqry_rechash_from_locid = select(harm_location_to_rec.fk_data_record).distinct()
            subqry_rechash_from_locid = subqry_rechash_from_locid.where(harm_location_to_rec.fk_harm_location == location_id)
            # rtd = record_hash to datatype
            subqry_rtd_i = select(harmonized_int.fk_data_type).distinct().where(harmonized_int.fk_data_record.in_(subqry_rechash_from_locid))
            subqry_rtd_ic = select(harmonized_int_confidence.fk_data_type).distinct().where(harmonized_int_confidence.fk_data_record.in_(subqry_rechash_from_locid))
            subqry_rtd_f = select(harmonized_float.fk_data_type).distinct().where(harmonized_float.fk_data_record.in_(subqry_rechash_from_locid))
            subqry_rtd_fc = select(harmonized_float_confidence.fk_data_type).distinct().where(harmonized_float_confidence.fk_data_record.in_(subqry_rechash_from_locid))
            subqry_rtd_u = union(subqry_rtd_i, subqry_rtd_ic, subqry_rtd_f, subqry_rtd_fc)
            stmt = stmt.where(harm_data_type.datatype_id.in_(subqry_rtd_u))
        if active_datatypes is not None:
            logger.debug("•• active_datatypes is not none")
            subqry_dt_i = select(harmonized_int.fk_data_type).distinct()
            subqry_dt_ic = select(harmonized_int_confidence.fk_data_type).distinct()
            subqry_dt_f = select(harmonized_float.fk_data_type).distinct()
            subqry_dt_fc = select(harmonized_float_confidence.fk_data_type).distinct()
            stmt = stmt.where(harm_data_type.datatype_id.in_(union(subqry_dt_f, subqry_dt_fc, subqry_dt_i, subqry_dt_ic)))
        results = shared_execution.list(stmt=stmt, pydantic_object=HARM_Data_Type, session_object=session, output_format="application/json")
    return results

def get_harm_data_type(
    datatype_id: Optional[UUID] = None,
    pk_harm_data_type: Optional[int] = None
) -> HARM_Data_Type:
    logger.debug(f"{fa.service}{fa.get} {__name__}  {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_data_type)
        if datatype_id is not None:
            stmt = stmt.where(harm_data_type.datatype_id == datatype_id)
        if pk_harm_data_type is not None:
            stmt = stmt.where(harm_data_type.pk_harm_data_type == pk_harm_data_type)
        result = session.execute(stmt).first()
    return HARM_Data_Type(**result.tuple()[0].__dict__)


def create_harm_data_type(new_harm_data_type: HARM_Data_Type) -> HARM_Data_Type:
    logger.debug(f"{fa.service}{fa.create} {__name__}  {stack()[0][3]}()")
    if "datatype_id" not in new_harm_data_type.model_fields_set:
        new_harm_data_type.datatype_id = uuid4()
    if new_harm_data_type.datatype_id is None:
        new_harm_data_type.datatype_id = uuid4()
    with Session(engine) as session:
        stmt = insert(harm_data_type)
        stmt = stmt.values(**new_harm_data_type.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return_harm_data_type = get_harm_data_type(
        pk_harm_data_type=execute.inserted_primary_key[0]
    )
    new_data_type_uuid = return_harm_data_type.datatype_id
    new_data_type_uuid = new_data_type_uuid.hex
    with Session(engine) as session:
        numericals = [
            harm_data_numerical.harmonized_int,
            harm_data_numerical.harmonized_int_confidence,
            harm_data_numerical.harmonized_float,
            harm_data_numerical.harmonized_float_confidence,
        ]
        numericals = [x.__tablename__ for x in numericals]
        for partitioner in numericals:
            stmt = text(f"""CREATE TABLE {partitioner}_{new_data_type_uuid} PARTITION
                        OF {partitioner} FOR VALUES IN ('{new_data_type_uuid}');""")
            session.execute(stmt)
            session.commit()
    return return_harm_data_type


def update_harm_data_type(update_harm_data_type: HARM_Data_Type) -> HARM_Data_Type:
    logger.debug(f"{fa.service}{fa.update} {__name__}  {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = update(harm_data_type)
        stmt = stmt.where(
            harm_data_type.datatype_id == update_harm_data_type.datatype_id
        )
        stmt = stmt.values(update_harm_data_type)
        execute = session.execute(stmt)
        commit = session.commit()
    return get_harm_data_type(datatype_id=update_harm_data_type.datatype_id)


def delete_harm_data_type(datatype_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__}  {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_data_type)
        logger.debug(datatype_id)
        stmt = stmt.where(harm_data_type.datatype_id == datatype_id)
        execute = session.execute(stmt)
        commit = session.commit()
    return None


def assign_datatype_to_dataset(datatype_id: UUID,
                               dataset_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__}  {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(datatype_to_dataset)
        stmt = stmt.values(
            fk_datatype_id=datatype_id,
            fk_dataset_id=dataset_id
        )
        execute = session.execute(stmt)
        commit = session.commit()

def remove_datatype_from_dataset(datatype_id: UUID,
                               dataset_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__}  {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(datatype_to_dataset)
        stmt = stmt.where(datatype_to_dataset.fk_dataset_id==dataset_id)
        stmt = stmt.where(datatype_to_dataset.fk_datatype_id==datatype_id)
        execute = session.execute(stmt)
        commit = session.commit()