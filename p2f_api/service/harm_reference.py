# Batteries included libraries
from typing import List, Optional
from uuid import UUID, uuid4
from inspect import stack

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from sqlalchemy import union

# Local libraries
from p2f_api.apilogs import logger, fa
from service import shared_execution
from ..data.db_connection import engine
from ..data.harm_reference import harm_reference, harm_reference_to_record, harm_reference_to_dataset
from ..data.harm_data_record import harm_data_record
from ..data.harm_data_numerical import harmonized_int, harmonized_int_confidence
from ..data.harm_data_numerical import harmonized_float, harmonized_float_confidence
from ..data.harm_locations import harm_location_to_rec, harm_location_to_ds
from p2f_pydantic.harm_reference import HARM_Reference

# List
def list_references(dataset_id: UUID | None = None,
                    record_hash: str | None = None, 
                    datatype_id: UUID | None = None,
                    location_id: UUID | None = None,
                    output_format: shared_execution.mimes = "application/json",) -> List[HARM_Reference]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_reference)
        if dataset_id is not None:
            subqry_ds_recs = select(harm_data_record.record_hash).distinct().where(harm_data_record.fk_dataset == dataset_id)
            subqry_ds_recs_refs = select(harm_reference_to_record.fk_harm_reference).distinct().where(harm_reference_to_record.fk_record_hash.in_(subqry_ds_recs))
            subqry_ds_refs = select(harm_reference_to_dataset.fk_harm_reference).distinct().where(harm_reference_to_dataset.fk_dataset_id == dataset_id)
            subqry_ds_union = union(subqry_ds_recs_refs, subqry_ds_refs)
            stmt = stmt.where(harm_reference.reference_id.in_(subqry_ds_union))
        if record_hash is not None:
            subqry_rec_refs = select(harm_reference_to_record.fk_harm_reference).distinct().where(harm_reference_to_record.fk_record_hash == record_hash)
            stmt = stmt.where(harm_reference.reference_id.in_(subqry_rec_refs))
        if datatype_id is not None:
            subqry_i = select(harmonized_int.fk_data_record).distinct().where(harmonized_int.fk_data_type == datatype_id)
            subqry_ic = select(harmonized_int_confidence.fk_data_record).distinct().where(harmonized_int_confidence.fk_data_type == datatype_id)
            subqry_f = select(harmonized_float.fk_data_record).distinct().where(harmonized_float.fk_data_type == datatype_id)
            subqry_fc = select(harmonized_float_confidence.fk_data_record).distinct().where(harmonized_float_confidence.fk_data_type == datatype_id)
            subqry_u = union(subqry_i, subqry_ic, subqry_f, subqry_fc)
            subqry_dt_rec_refs = select(harm_reference_to_record.fk_harm_reference).distinct().where(harm_reference_to_record.fk_record_hash.in_(subqry_u))
            stmt = stmt.where(subqry_dt_rec_refs)
        if location_id is not None:
            subqry_loc_rec = select(harm_location_to_rec.fk_data_record).distinct().where(harm_location_to_rec.fk_harm_location == location_id)
            subqry_loc_ds = select(harm_location_to_ds.fk_dataset_id).distinct().where(harm_location_to_ds.fk_harm_location == location_id)
            subqry_loc_rec_refs = select(harm_reference_to_record.fk_record_hash).distinct().where(harm_reference_to_record.fk_record_hash.in_(subqry_loc_rec))
            subqry_loc_ds_refs = select(harm_reference_to_dataset.fk_harm_reference).distinct().where(harm_reference_to_dataset.fk_dataset_id.in_(subqry_loc_ds))
            subqry_loc_u = union(subqry_loc_rec_refs, subqry_loc_ds_refs)
            stmt = stmt.where(harm_reference.reference_id.in_(subqry_loc_u))
        results = shared_execution.list(stmt=stmt,
                                        pydantic_object=HARM_Reference,
                                        session_object=session,
                                        output_format=output_format)
    return results


# Get
def get_reference(
    doi: Optional[str] = None,
    reference_id: Optional[str] = None,
    pk_harm_reference: Optional[int] = None,
    output_format: shared_execution.mimes = "application/json",
) -> HARM_Reference:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_reference)
        if doi is not None:
            stmt = stmt.where(harm_reference.doi == doi)
        if reference_id is not None:
            stmt = stmt.where(harm_reference.reference_id == reference_id)
        if pk_harm_reference is not None:
            stmt = stmt.where(harm_reference.pk_harm_reference == pk_harm_reference)
        result = shared_execution.get(stmt=stmt, 
                                      pydantic_object=HARM_Reference,
                                      session_object=session,
                                      output_format=output_format)
    return result


# Create
def create_reference(new_reference: HARM_Reference,
                     output_format: shared_execution.mimes = "application/json",) -> HARM_Reference:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    if new_reference.reference_id is None:
        new_reference.reference_id = uuid4()
    with Session(engine) as session:
        stmt = insert(harm_reference)
        stmt = stmt.values(**new_reference.model_dump(exclude_unset=True))
        pk = shared_execution.create(stmt=stmt, session_object=session)
    return get_reference(pk_harm_reference=pk, 
                         output_format=output_format)


# Update


# Delete
def delete_reference(reference_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_reference)
        stmt = stmt.where(reference_id == reference_id)
        shared_execution.delete(stmt=stmt, session_object=session)
    return None


# Assign
def assign_reference(reference_id: UUID,
                     record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.assign} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(harm_reference_to_record)
        stmt = stmt.values(fk_harm_reference=reference_id, fk_record_hash=record_hash)
        execute = session.execute(stmt)
        commit = session.commit()


# Remove
def remove_reference(reference_id: UUID, 
                     record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.remove} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_reference_to_record)
        stmt = stmt.where(harm_reference_to_record.fk_harm_reference == reference_id)
        stmt = stmt.where(harm_reference_to_record.fk_record_hash == record_hash)
        execute = session.execute(stmt)
        commit = session.commit()
