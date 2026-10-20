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
from ..data.harm_core import core, coreSegment, coreSegment_to_record
from p2f_pydantic.harm_core import Core, CoreSegment


def list_cores(output_format: shared_execution.mimes = "application/json",) -> List[Core]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(core)
        results = shared_execution.list(stmt=stmt,
                                        pydantic_object=Core,
                                        session_object=session,
                                        output_format=output_format)
    return results

def list_core_segments(core_id: UUID,
                       output_format: shared_execution.mimes = "application/json",) -> List[CoreSegment]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(coreSegment)
        stmt = stmt.where(coreSegment.fk_core_id == core_id)
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