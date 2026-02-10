# Local libraries
from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.harm_reference import harm_reference, harm_reference_to_record
from p2f_pydantic.harm_reference import harm_reference as Harm_reference
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Optional
from uuid import UUID


# List
def list_references() -> List[Harm_reference]:
    logger.debug(f"{fa.service}{fa.list} {__name__}")
    with Session(engine) as session:
        stmt = select(harm_reference)
        results = session.execute(stmt).all()
    return [Harm_reference(**x[0].__dict__) for x in results]

# Get
def get_reference(doi: Optional[str]=None, 
                  reference_id: Optional[str]=None,
                  pk_harm_reference: Optional[int]=None) -> Harm_reference:
    logger.debug(f"{fa.service}{fa.get} {__name__}")
    with Session(engine) as session:
        stmt = select(harm_reference)
        if doi is not None:
            stmt = stmt.where(harm_reference.doi==doi)
        if reference_id is not None:
            stmt = stmt.where(harm_reference.reference_id==reference_id)
        if pk_harm_reference is not None:
            stmt = stmt.where(harm_reference.pk_harm_reference==pk_harm_reference)
        result = session.execute(stmt).first()
    return Harm_reference(**result.tuple()[0].__dict__)

# Create
def create_reference(new_reference: Harm_reference) -> Harm_reference:
    logger.debug(f"{fa.service}{fa.create} {__name__}")
    with Session(engine) as session:
        stmt = insert(harm_reference)
        stmt = stmt.values(**new_reference.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return get_reference(pk_harm_reference=execute.inserted_primary_key[0])

# Update

# Delete
def delete_reference(reference_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__}")
    with Session(engine) as session:
        stmt = delete(harm_reference)
        stmt = stmt.where(reference_id == reference_id)
        execute = session.execute(stmt)
        commit = session.commit()
    return None

# Assign
def assign_reference(reference_id: UUID, 
                     record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.assign} {__name__}")
    with Session(engine) as session:
        stmt = insert(harm_reference_to_record)
        stmt = stmt.values(fk_harm_reference=reference_id,
                           fk_record_hash=record_hash)
        execute = session.execute(stmt)
        commit = session.commit()

# Remove
def remove_reference(reference_id: UUID, 
                     record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.remove} {__name__}")
    with Session(engine) as session: 
        stmt = delete(harm_reference_to_record)
        stmt = stmt.where(harm_reference_to_record.fk_harm_reference==reference_id)
        stmt = stmt.where(harm_reference_to_record.fk_record_hash==record_hash)
        execute = session.execute(stmt)
        commit = session.commit()
