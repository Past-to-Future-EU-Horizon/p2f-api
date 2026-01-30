from p2f_api.apilogs import logger
from ..data.db_connection import engine
from ..data.harm_data_metadata import harm_location_to_record, harm_locations
from p2f_pydantic.harm_data_metadata import harm_location as Harm_location
from p2f_pydantic.harm_data_metadata import harm_bounding_box as Harm_bounding_box
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Optional
from uuid import UUID

def list_harm_metadata_location(
        bounding_box: Optional[Harm_bounding_box]=None,
        location_name: Optional[str]=None, 
        location_code: Optional[str]=None, 
        minimum_elevation: Optional[float]=None,
        maximum_elevation: Optional[float]=None,
        min_location_age: Optional[float]=None,
        max_location_age: Optional[float]=None,
    ) -> List[Harm_location]:
    with Session(engine) as session:
        stmt = select(harm_locations)
        if bounding_box is not None:
            stmt = stmt.where(harm_locations.latitude <= bounding_box.north)
            stmt = stmt.where(harm_locations.latitude >= bounding_box.south)
            stmt = stmt.where(harm_locations.longitude <= bounding_box.east)
            stmt = stmt.where(harm_locations.longitude >= bounding_box.west)
        if location_name is not None:
            stmt = stmt.where(harm_locations.location_name == location_name)
        if location_code is not None:
            stmt = stmt.where(harm_locations.location_code == location_code)
        if minimum_elevation is not None:
            stmt = stmt.where(harm_locations.elevation >= minimum_elevation)
        if maximum_elevation is not None:
            stmt = stmt.where(harm_locations.elevation <= maximum_elevation)
        if min_location_age is not None:
            stmt = stmt.where(harm_locations.location_age >= min_location_age)
        if max_location_age is not None:
            stmt = stmt.where(harm_locations.location_age <= max_location_age)
        results = session.execute(stmt)
    return [Harm_location(**x[0].__dict__) for x in results]

def get_location(location_identifier: Optional[UUID]=None,
                 pk_harm_location: Optional[int]=None) -> Harm_location:
    with Session(engine) as session:
        stmt = select(harm_locations)
        if location_identifier is not None:
            stmt = stmt.where(harm_locations.location_identifier == location_identifier)
        if pk_harm_location is not None:
            stmt = stmt.where(harm_locations.pk_harm_location==pk_harm_location)
        result = session.execute(stmt).first()
    result = result.tuple()[0]
    return Harm_location(**result.__dict__)

def create_location(new_location: Harm_location) -> Harm_location:
    with Session(engine) as session:
        stmt = insert(harm_locations)
        stmt = stmt.values(**new_location.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return get_location(pk_harm_location=execute.inserted_primary_key[0])

def update_location(update_location: Harm_location) -> Harm_location:
    with Session(engine) as session:
        stmt = update(harm_locations)
        stmt = stmt.where(update_location.location_identifier)
        stmt = stmt.values(update_location)
        execute = session.execute(stmt)
        commit = session.commit()
    return get_location(update_location.pk_harm_location)

def delete_location(location_identifier: UUID) -> None:
    with Session(engine) as session:
        stmt = delete(harm_locations)
        stmt = stmt.where(harm_locations.location_identifier == location_identifier)
        execute = session.execute(stmt)
        commit = session.commit()
    return None

def assign_location_to_record(
        location_identifier: UUID,
        record_hash: str
    ): 
    logger.debug("harm_data_metadata_location.py assign_location_to_record()")
    with Session(engine) as session:
        logger.debug("Session created")
        stmt = insert(harm_location_to_record)
        stmt = stmt.values(
            {"fk_harm_location": location_identifier,
             "fk_data_record": record_hash}
        )
        logger.debug(stmt)
        execute = session.execute(stmt)
        commit = session.commit()
    return None

def remove_location_from_record(
        location_identifier: UUID,
        record_hash: str
    ): 
    with Session(engine) as session:
        stmt = delete(harm_location_to_record)
        stmt = stmt.where(harm_location_to_record.fk_data_record == record_hash)
        stmt = stmt.where(harm_location_to_record.fk_harm_location == location_identifier)
        execute = session.execute(stmt)
        commit = session.commit()
    return None