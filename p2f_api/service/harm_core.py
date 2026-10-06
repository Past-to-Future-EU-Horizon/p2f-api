# Batteries included libraries
from typing import List, Optional
from uuid import UUID
from inspect import stack

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update

# Local libraries
from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.harm_core import core, coreSegment
from p2f_pydantic.harm_core import Core, CoreSegment


def list_cores() -> List[Core]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(core)
        result = session.execute(stmt).all()
    return [Core(**x) for x in result]

def list_core_segments(core_id: UUID) -> List[CoreSegment]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(coreSegment)
        stmt = stmt.where(coreSegment.fk_core_id == core_id)
        result = session.execute(stmt).all()
    return [CoreSegment(**x) for x in result]

def get_core(core_id: UUID | None=None,
             pk_core: int | None=None) -> Core:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(core)
        if core_id:
            stmt = stmt.where(core.core_id == core_id)
        if pk_core:
            stmt = stmt.where(core.pk_harm_core == pk_core)
        result = session.execute(stmt).first()
    return Core(**result)

def get_core_segment(core_id: UUID | None = None,
                     core_segment_id: UUID | None=None,
                     pk_core_segment: int | None=None) -> CoreSegment:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(coreSegment)
        if core_id:
            stmt = stmt.where(coreSegment.fk_core_id == core_id)
        if core_segment_id:
            stmt = stmt.where(coreSegment.core_segment_id == core_segment_id)
        if pk_core_segment:
            stmt = stmt.where(coreSegment.pk_harm_core_segment == pk_core_segment)
        result = session.execute(stmt).first()
    return CoreSegment(**result)

def create_core(new_core: Core) -> Core:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(core)
        stmt = stmt.values(**new_core.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return get_core(pk_core=execute.inserted_primary_key[0])

def create_core_segment(core_id: UUID, 
                        new_core_segment: CoreSegment) -> CoreSegment:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    if core_id == new_core_segment.fk_core_id:
        with Session(engine) as session:
            stmt = insert(coreSegment)
            stmt = stmt.values(**new_core_segment.model_dump(exclude_unset=True))
            execute = session.execute(stmt)
            commit = session.commit()
        return get_core_segment(pk_core_segment=execute.inserted_primary_key[0])
    else: 
        raise ValueError("supplied core_id did not match the core_id in the new segment")

def delete_core(core_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(core)
        stmt = stmt.where(core.core_id == core_id)
        execute = session.execute(stmt)
        commit = session.commit()

def delete_core_segment(core_id: UUID, 
                        core_segment_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(coreSegment)
        # we don't need to do a check here if core_id ==  core_segment_id.fk_core_id 
        # because if they don't match nothing will happen
        stmt = stmt.where(coreSegment.fk_core_id == core_id)
        stmt = stmt.where(coreSegment.core_segment_id == core_segment_id)
        execute = session.execute(stmt)
        commit = session.commit()
