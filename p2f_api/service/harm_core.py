# Batteries included libraries
from typing import List, Optional, Literal
from uuid import UUID
from inspect import stack

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from sqlalchemy import union

# Local libraries
from p2f_api.apilogs import logger, fa
from service import shared_execution
from ..data.db_connection import engine
from ..data.harm_core import core, coreSegment, coreSegment_to_record
from ..data.harm_data_record import harm_data_record
from ..data.harm_data_numerical import harmonized_int, harmonized_int_confidence
from ..data.harm_data_numerical import harmonized_float, harmonized_float_confidence
from p2f_pydantic.harm_core import Core, CoreSegment


def list_cores(dataset_id: UUID | None = None,
               record_hash: str | None = None,
               active_core: bool | None = None,
               location_id: UUID | None = None, 
               datatype_id: UUID | None = None,
               core_type: Literal["ice", "sediment", "other"] | None = None,
               output_format: shared_execution.mimes = "application/json",) -> List[Core]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(core)
        if core_type is not None:
            stmt = stmt.where(core.core_type == core_type)
        if record_hash is not None: 
            # Select the coreSegments that are assigned to a record
            coreseg_assigned_subqry = select(coreSegment_to_record.fk_core_segment_id.distinct())
            coreseg_assigned_subqry = coreseg_assigned_subqry.where(coreSegment_to_record.fk_record_hash == record_hash)
            # Select the core segment using the above record query
            coreseg_subqry = select(coreSegment.fk_core_id.distinct())
            coreseg_subqry = coreseg_subqry.where(coreSegment.core_segment_id.in_(coreseg_assigned_subqry))
            # select core
            stmt = stmt.where(core.core_id.in_(coreseg_subqry))
        if dataset_id is not None:
            # Select the record hashes where the record hash are associated with the dataset_id
            dataset_subqry = select(harm_data_record.record_hash).distinct()
            dataset_subqry = dataset_subqry.where(harm_data_record.fk_dataset == dataset_id)
            # select the core segment id that are matched to the above record hashes
            core_segments_rel_subqry = select(coreSegment_to_record.fk_core_segment_id).distinct()
            core_segments_rel_subqry = core_segments_rel_subqry.where(coreSegment_to_record.in_(dataset_subqry))
            # select the core_ids from the core_segments
            coreseg_dataset_subqry = select(coreSegment.fk_core_id).distinct()
            coreseg_dataset_subqry = coreseg_dataset_subqry.where(coreSegment.core_segment_id.in_(core_segments_rel_subqry))
            # finally get the cores
            stmt = stmt.where(core.core_id.in_(coreseg_dataset_subqry))
        if active_core is not None:
            # get all distinct assigned core_segment_id
            assigned_segments_subqry = select(coreSegment_to_record.fk_core_segment_id).distinct()
            # get related parent core from core_segment_ids
            coreseg_assigned_subqry = select(coreSegment.fk_core_id).distinct()
            coreseg_assigned_subqry = coreseg_assigned_subqry.where(coreSegment.core_segment_id.in_(assigned_segments_subqry))
            # filter cores by above
            stmt = stmt.where(core.core_id.in_(coreseg_assigned_subqry))
        if location_id is not None:
            stmt = stmt.where(core.fk_location == location_id)
        if datatype_id is not None:
            # Request all numerics by data type
            subqry_i_rec = select(harmonized_int.fk_data_record).distinct().where(harmonized_int.fk_data_type == datatype_id)
            subqry_ic_rec = select(harmonized_int_confidence.fk_data_record).distinct().where(harmonized_int_confidence.fk_data_type == datatype_id)
            subqry_f_rec = select(harmonized_float.fk_data_record).distinct().where(harmonized_float.fk_data_type == datatype_id)
            subqry_fc_rec = select(harmonized_float_confidence.fk_data_record).distinct().where(harmonized_float_confidence.fk_data_type == datatype_id)
            # group numerics
            subqry_union_rec = union(subqry_i_rec, subqry_ic_rec, subqry_f_rec, subqry_fc_rec)
            # match core segment ids with the record hashes
            coresegs_union_subqry = select(coreSegment_to_record.fk_core_segment_id).distinct()
            coresegs_union_subqry = coresegs_union_subqry.where(coreSegment_to_record.fk_record_hash.in_(subqry_union_rec))
            # get the cores from the above matched core segments
            coreseg_dtype_subqry = select(coreSegment.fk_core_id).distinct()
            coreseg_dtype_subqry = coreseg_dtype_subqry.where(coreSegment.core_segment_id.in_(coresegs_union_subqry))
            # filter by core ids
            stmt = stmt.where(core.core_id.in_(coreseg_dtype_subqry))
        results = shared_execution.list(stmt=stmt,
                                        pydantic_object=Core,
                                        session_object=session,
                                        output_format=output_format)
    return results

def list_core_segments(core_id: UUID | None = None,
                       dataset_id: UUID | None = None,
                       record_hash: str | None = None,
                       location_id: UUID | None = None,
                       datatype_id: UUID | None = None,
                       active_segments: bool | None = None,                       
                       output_format: shared_execution.mimes = "application/json",) -> List[CoreSegment]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(coreSegment)
        if core_id is not None:
            stmt = stmt.where(coreSegment.fk_core_id == core_id)
        if dataset_id is not None:
            # Request record hashes that are associated with dataset
            rechash_datasetid_subqry = select(harm_data_record.record_hash).distinct()
            rechash_datasetid_subqry = rechash_datasetid_subqry.where(harm_data_record.fk_dataset == dataset_id)
            # Match record hashes to coreSegments
            coreseg_rechash_subqry = select(coreSegment_to_record.fk_core_segment_id).distinct()
            coreseg_rechash_subqry = coreseg_rechash_subqry.where(coreSegment_to_record.fk_record_hash.in_(rechash_datasetid_subqry))
            # Filter by these core segments
            stmt = stmt.where(coreSegment.core_segment_id.in_(coreseg_rechash_subqry))
        if record_hash is not None:
            # Match record hash to coreSegments
            rechash_coreseg_subqry = select(coreSegment_to_record.fk_core_segment_id).distinct()
            rechash_coreseg_subqry = rechash_coreseg_subqry.where(coreSegment_to_record.fk_record_hash == record_hash)
            # Filter by coreSegments
            stmt = stmt.where(coreSegment.core_segment_id.in_(rechash_coreseg_subqry))
        if location_id is not None:
            # Get core_id at location
            location_core_subqry = select(core.core_id).distinct()
            location_core_subqry = location_core_subqry.where(core.fk_location == location_id)
            # Get CoreSegments with above core_id
            stmt = stmt.where(coreSegment.fk_core_id.in_(location_core_subqry))
        if datatype_id is not None:
            # Gather numeric distinct numeric record hashes
            subqry_i_rec = select(harmonized_int.fk_data_record).distinct().where(harmonized_int.fk_data_type == datatype_id)
            subqry_ic_rec = select(harmonized_int_confidence.fk_data_record).distinct().where(harmonized_int_confidence.fk_data_type == datatype_id)
            subqry_f_rec = select(harmonized_float.fk_data_record).distinct().where(harmonized_float.fk_data_type == datatype_id)
            subqry_fc_rec = select(harmonized_float_confidence.fk_data_record).distinct().where(harmonized_float_confidence.fk_data_type == datatype_id)
            # group them up
            subqry_union_rec = union(subqry_i_rec, subqry_ic_rec, subqry_f_rec, subqry_fc_rec)
            # match record hashes to core segment ids
            dtype_rechash_subqry = select(coreSegment_to_record.fk_core_segment_id).distinct()
            dtype_rechash_subqry = dtype_rechash_subqry.where(coreSegment_to_record.fk_record_hash.in_(subqry_union_rec))
            # filter by core segment ids
            stmt = stmt.where(coreSegment.core_segment_id.in_(dtype_rechash_subqry))
        if active_segments is not None:
            # gather assigned core_segments
            subqry_coresegs_inuse = select(coreSegment_to_record.fk_core_segment_id).distinct()
            stmt = stmt.where(coreSegment.core_segment_id.in_(subqry_coresegs_inuse))
        results = shared_execution.list(stmt=stmt,
                                        pydantic_object=CoreSegment,
                                        session_object=session,
                                        output_format=output_format)
    return results

def get_core(core_id: UUID | None=None,
             pk_core: int | None=None,
             output_format: shared_execution.mimes = "application/json",) -> Core:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(core)
        if core_id:
            stmt = stmt.where(core.core_id == core_id)
        if pk_core:
            stmt = stmt.where(core.pk_harm_core == pk_core)
        result = shared_execution.get(stmt=stmt,
                                      pydantic_object=Core, 
                                      session_object=session,
                                      output_format=output_format)
    return result

def get_core_segment(core_id: UUID | None = None,
                     core_segment_id: UUID | None=None,
                     pk_core_segment: int | None=None,
                     output_format: shared_execution.mimes = "application/json",) -> CoreSegment:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(coreSegment)
        if core_id:
            stmt = stmt.where(coreSegment.fk_core_id == core_id)
        if core_segment_id:
            stmt = stmt.where(coreSegment.core_segment_id == core_segment_id)
        if pk_core_segment:
            stmt = stmt.where(coreSegment.pk_harm_core_segment == pk_core_segment)
        result = shared_execution.get(stmt=stmt, 
                                      pydantic_object=CoreSegment,
                                      session_object=session,
                                      output_format=output_format)
    return result

def create_core(new_core: Core,
                output_format: shared_execution.mimes = "application/json",) -> Core:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(core)
        stmt = stmt.values(**new_core.model_dump(exclude_unset=True))
        pk = shared_execution.create(stmt=stmt, 
                                     session_object=session)
    return get_core(pk_core=pk, 
                    output_format=output_format)

def create_core_segment(core_id: UUID, 
                        new_core_segment: CoreSegment,
                        output_format: shared_execution.mimes = "application/json",) -> CoreSegment:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    if core_id == new_core_segment.fk_core_id:
        with Session(engine) as session:
            stmt = insert(coreSegment)
            stmt = stmt.values(**new_core_segment.model_dump(exclude_unset=True))
            pk = shared_execution.create(stmt=stmt,
                                         session_object=session)
        return get_core_segment(pk_core_segment=pk,
                                output_format=output_format)
    else: 
        raise ValueError("supplied core_id did not match the core_id in the new segment")

def delete_core(core_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(core)
        stmt = stmt.where(core.core_id == core_id)
        shared_execution.delete(stmt=stmt, 
                                session_object=session)

def delete_core_segment(core_id: UUID, 
                        core_segment_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(coreSegment)
        # we don't need to do a check here if core_id ==  core_segment_id.fk_core_id 
        # because if they don't match nothing will happen
        stmt = stmt.where(coreSegment.fk_core_id == core_id)
        stmt = stmt.where(coreSegment.core_segment_id == core_segment_id)
        shared_execution.delete(stmt=stmt,
                                session_object=session)

def assign_core_segment_to_record(core_segment_id: UUID,
                                  record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.assign} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(coreSegment_to_record)
        stmt = stmt.values(
            fk_record_hash=record_hash,
            fk_core_segment_id=core_segment_id
        )
        execute = session.execute(stmt)
        commit = session.commit()

def remove_core_segment_from_record(core_segment_id: UUID,
                                    record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.remove} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(coreSegment_to_record)
        stmt = stmt.where(coreSegment_to_record.fk_record_hash == record_hash)
        stmt = stmt.where(coreSegment_to_record.fk_core_segment_id == core_segment_id)
        execute = session.execute(stmt)
        commit = session.commit()