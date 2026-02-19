from p2f_api.apilogs import logger, fa
from .harm_data_record import list_harm_data_record
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
from inspect import stack


def list_harm_metadata_location(
    bounding_box: Optional[Harm_bounding_box] = None,
    location_name: Optional[str] = None,
    location_code: Optional[str] = None,
    minimum_elevation: Optional[float] = None,
    maximum_elevation: Optional[float] = None,
    min_location_age: Optional[float] = None,
    max_location_age: Optional[float] = None,
    dataset_id: Optional[float] = None,
) -> List[Harm_location]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    if dataset_id is not None:
        logger.debug(f"•  Dataset_id is not None: {dataset_id}")
        data_record_list = list_harm_data_record(dataset=dataset_id)
        logger.debug(f"•• Data records found for dataset_id: {data_record_list}")
        data_record_list = [x.record_hash for x in data_record_list]
        logger.debug(f"•• Reformatted records list: {data_record_list}")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = select(harm_locations)
        if bounding_box is not None:
            logger.debug("•• Bounding box is not none")
            stmt = stmt.where(harm_locations.latitude <= bounding_box.north)
            stmt = stmt.where(harm_locations.latitude >= bounding_box.south)
            stmt = stmt.where(harm_locations.longitude <= bounding_box.east)
            stmt = stmt.where(harm_locations.longitude >= bounding_box.west)
        if location_name is not None:
            logger.debug("•• Location name is not none")
            stmt = stmt.where(harm_locations.location_name == location_name)
        if location_code is not None:
            logger.debug("•• Location code is not none")
            stmt = stmt.where(harm_locations.location_code == location_code)
        if minimum_elevation is not None:
            logger.debug("•• Minimum elevation is not none")
            stmt = stmt.where(harm_locations.elevation >= minimum_elevation)
        if maximum_elevation is not None:
            logger.debug("•• Maximum elevation is not none")
            stmt = stmt.where(harm_locations.elevation <= maximum_elevation)
        if min_location_age is not None:
            logger.debug("•• Minimum location age is not none")
            stmt = stmt.where(harm_locations.location_age >= min_location_age)
        if max_location_age is not None:
            logger.debug("•• Maximum location age is not none")
            stmt = stmt.where(harm_locations.location_age <= max_location_age)
        if dataset_id is not None:
            logger.debug("•• Dataset id is not none")
            subqry = select(harm_location_to_record.fk_harm_location).where(
                harm_location_to_record.fk_data_record.in_(data_record_list)
            )
            stmt = stmt.where(harm_locations.location_identifier.in_(subqry))
            logger.debug(f"•• Dataset identifier statement alteration: {stmt}")
        results = session.execute(stmt).all()
        logger.debug(f"• Found {len(results)} results. ")
    return [Harm_location(**x[0].__dict__) for x in results]


def get_location(
    location_identifier: Optional[UUID] = None, 
    pk_harm_location: Optional[int] = None
) -> Harm_location:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_locations)
        if location_identifier is not None:
            stmt = stmt.where(harm_locations.location_identifier == location_identifier)
        if pk_harm_location is not None:
            stmt = stmt.where(harm_locations.pk_harm_location == pk_harm_location)
        result = session.execute(stmt).first()
    result = result.tuple()[0]
    return Harm_location(**result.__dict__)


def create_location(new_location: Harm_location) -> Harm_location:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(harm_locations)
        stmt = stmt.values(**new_location.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return get_location(pk_harm_location=execute.inserted_primary_key[0])


def update_location(update_location: Harm_location) -> Harm_location:
    logger.debug(f"{fa.service}{fa.update} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = update(harm_locations)
        stmt = stmt.where(update_location.location_identifier)
        stmt = stmt.values(update_location)
        execute = session.execute(stmt)
        commit = session.commit()
    return get_location(update_location.pk_harm_location)


def delete_location(location_identifier: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_locations)
        stmt = stmt.where(harm_locations.location_identifier == location_identifier)
        execute = session.execute(stmt)
        commit = session.commit()
    return None


def assign_location_to_record(location_identifier: UUID, record_hash: str):
    logger.debug(f"{fa.service}{fa.assign} {__name__} {stack()[0][3]}()")
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


def remove_location_from_record(location_identifier: UUID, record_hash: str):
    logger.debug(f"{fa.service}{fa.remove} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_location_to_record)
        stmt = stmt.where(harm_location_to_record.fk_data_record == record_hash)
        stmt = stmt.where(
            harm_location_to_record.fk_harm_location == location_identifier
        )
        execute = session.execute(stmt)
        commit = session.commit()
    return None
