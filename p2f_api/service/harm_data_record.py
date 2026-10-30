# Batteries included libraries
from typing import List, Optional
from uuid import UUID
from inspect import stack

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from sqlalchemy import union

# Local libraries
from p2f_api.apilogs import logger, fa
from service import shared_execution
# from ..service.harm_numerical import list_numerics
from ..data.db_connection import engine
from ..data.harm_data_record import harm_data_record
from ..data.harm_data_numerical import harmonized_int, harmonized_int_confidence
from ..data.harm_data_numerical import harmonized_float, harmonized_float_confidence
from ..data.harm_locations import harm_location_to_rec, harm_location_to_ds
from ..data.harm_core import coreSegment, coreSegment_to_record
from p2f_pydantic.harm_data_record import HARM_Data_Record


def list_harm_data_record(
    dataset_id: Optional[UUID] = None,
    datatype_id: Optional[UUID] = None,
    location_id: Optional[UUID] = None,
    core_id: Optional[UUID] = None,
    core_segment_id: Optional[UUID] = None,
    output_format: shared_execution.mimes = "application/json",
) -> List[HARM_Data_Record]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(harm_data_record)
        if dataset_id is not None:
            stmt = stmt.where(harm_data_record.fk_dataset == dataset_id)
        if datatype_id is not None:
            subqry_rechash_i = select(harmonized_int.fk_data_record).distinct().where(harmonized_int.fk_data_type == datatype_id)
            subqry_rechash_ic = select(harmonized_int_confidence.fk_data_record).distinct().where(harmonized_int_confidence.fk_data_type == datatype_id)
            subqry_rechash_f = select(harmonized_float.fk_data_record).distinct().where(harmonized_float.fk_data_type == datatype_id)
            subqry_rechash_fc = select(harmonized_float_confidence.fk_data_record).distinct().where(harmonized_float_confidence.fk_data_type == datatype_id)
            subqry_rechash_u = union(subqry_rechash_i, subqry_rechash_ic, subqry_rechash_f, subqry_rechash_fc)
            stmt = stmt.where(harm_data_record.record_hash.in_(subqry_rechash_u))
        if location_id is not None:
            subqry_loc_to_rec = select(harm_location_to_rec.fk_data_record).distinct().where(harm_location_to_rec.fk_harm_location == location_id)
            subqry_loc_to_ds = select(harm_location_to_ds.fk_dataset_id).distinct().where(harm_location_to_ds.fk_harm_location == location_id)
            subqry_ds_to_rec = select(harm_data_record.record_hash).distinct().where(harm_data_record.fk_dataset.in_(subqry_loc_to_ds))
            subqry_loc_union = union(subqry_loc_to_rec, subqry_ds_to_rec)
            stmt = stmt.where(harm_data_record.record_hash.in_(subqry_loc_union))
        if core_id is not None:
            subqry_coresegs = select(coreSegment.core_segment_id).distinct().where(coreSegment.fk_core_id == core_id)
            subqry_coreseg_rechash = select(coreSegment_to_record.fk_record_hash).distinct().where(coreSegment_to_record.fk_core_segment_id.in_(subqry_coresegs))
            stmt = stmt.where(harm_data_record.record_hash.in_(subqry_coreseg_rechash))
        if core_segment_id is not None:
            subqry_coreseg2rechash = select(coreSegment_to_record.fk_record_hash).distinct().where(coreSegment_to_record.fk_core_segment_id == core_segment_id)
            stmt = stmt.where(harm_data_record.record_hash.in_(subqry_coreseg2rechash))
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
