# Batteries included libraries
from typing import List, Optional
from uuid import UUID, uuid4
from inspect import stack

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from sqlalchemy import union

from p2f_api.apilogs import logger, fa
from service import shared_execution
from ..data.db_connection import engine
from ..data.harm_locations import harm_location_to_rec, harm_location_to_ds, harm_locations
from ..data.datasets import datasets as datasets_ddl
from ..data.harm_data_record import harm_data_record as harm_data_record_ddl
from ..data.harm_data_numerical import harmonized_int, harmonized_int_confidence
from ..data.harm_data_numerical import harmonized_float, harmonized_float_confidence
from p2f_pydantic.harm_location import HARM_Location
from p2f_pydantic.harm_location import HARM_Bounding_Box

def list_harm_metadata_location(
    bounding_box: Optional[HARM_Bounding_Box] = None,
    location_name: Optional[str] = None,
    location_code: Optional[str] = None,
    minimum_elevation: Optional[float] = None,
    maximum_elevation: Optional[float] = None,
    min_location_age: Optional[float] = None,
    max_location_age: Optional[float] = None,
    dataset_id: Optional[UUID] = None,
    datatype_id: UUID | None = None,
    record_hash: str | None = None,
    active_locations: Optional[bool] = None,
    output_format: shared_execution.mimes = "application/json",
) -> List[HARM_Location]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
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
            # Get dataset doi
            subqry_doi = select(datasets_ddl.doi)
            subqry_doi = subqry_doi.where(datasets_ddl.dataset_id == dataset_id)
            subqry_doi = subqry_doi.where(datasets_ddl.is_sub_dataset == False)
            # Get related datasets
            subqry_datasets = select(datasets_ddl.dataset_id).distinct()
            subqry_datasets = subqry_datasets.where(datasets_ddl.doi.in_(subqry_doi))
            # Get related location to dataset records
            subqry_loc_ds = select(harm_location_to_ds.fk_harm_location)
            subqry_loc_ds = subqry_loc_ds.where(harm_location_to_ds.fk_dataset_id.in_(subqry_datasets))
            # Get related datasets to record hashes
            subqry_recs = select(harm_data_record_ddl.record_hash).distinct()
            subqry_recs = subqry_recs.where(harm_data_record_ddl.fk_dataset.in_(subqry_datasets))
            # Get related locations to record hashes
            subqry_loc_rec = select(harm_location_to_rec.fk_harm_location)
            subqry_loc_rec.where(harm_location_to_rec.fk_data_record.in_(subqry_recs))
            stmt = stmt.where(harm_locations.location_id.in_(union(subqry_loc_ds, subqry_loc_rec)))
        if datatype_id is not None:
            logger.debug("•• Data Type id is not none")
            # Gather numeric distinct numeric record hashes
            subqry_i_rec = select(harmonized_int.fk_data_record).distinct().where(harmonized_int.fk_data_type == datatype_id)
            subqry_ic_rec = select(harmonized_int_confidence.fk_data_record).distinct().where(harmonized_int_confidence.fk_data_type == datatype_id)
            subqry_f_rec = select(harmonized_float.fk_data_record).distinct().where(harmonized_float.fk_data_type == datatype_id)
            subqry_fc_rec = select(harmonized_float_confidence.fk_data_record).distinct().where(harmonized_float_confidence.fk_data_type == datatype_id)
            # group them up
            subqry_union_rec = union(subqry_i_rec, subqry_ic_rec, subqry_f_rec, subqry_fc_rec)
            subqry_location_rec = select(harm_location_to_rec.fk_harm_location).distinct()
            subqry_location_rec = subqry_location_rec.where(harm_location_to_rec.fk_data_record.in_(subqry_union_rec))
            stmt = stmt.where(harm_locations.location_id.in_(subqry_location_rec))
        if record_hash is not None:
            logger.debug("•• Record Hash is not none")
            rechash_subqry = select(harm_location_to_rec.fk_harm_location).distinct()
            rechash_subqry = rechash_subqry.where(harm_location_to_rec.fk_data_record == record_hash)
            stmt = stmt.where(harm_locations.location_id.in_(rechash_subqry))
        if active_locations:
            logger.debug("•• active_locations id is not none or False")
            active_ds_subqry = select(harm_location_to_ds.fk_harm_location.distinct())
            active_rec_subqry = select(harm_location_to_rec.fk_harm_location.distinct())
            active_union = union(active_ds_subqry, active_rec_subqry)
            stmt = stmt.where(harm_locations.location_id.in_(active_union))
        results = shared_execution.list(stmt=stmt,
                                        pydantic_object=HARM_Location,
                                        session_object=session,
                                        output_format=output_format)
    return results


def get_location(
    location_id: Optional[UUID] = None, 
    record_hash: Optional[str] = None,
    pk_harm_location: Optional[int] = None,
    output_format: shared_execution.mimes = "application/json",
) -> HARM_Location:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(harm_locations)
        if location_id is not None:
            stmt = stmt.where(harm_locations.location_id == location_id)
        if record_hash is not None:
            subquery = select(harm_location_to_rec.fk_harm_location)
            subquery = subquery.where(harm_location_to_rec.fk_data_record == record_hash)
            stmt = stmt.where(harm_locations.location_id.in_(subquery))
        if pk_harm_location is not None:
            stmt = stmt.where(harm_locations.pk_harm_location == pk_harm_location)
        result = shared_execution.get(stmt=stmt,
                                      pydantic_object=HARM_Location,
                                      session_object=session,
                                      output_format=output_format)
    return result


def create_location(new_location: HARM_Location,
                    output_format: shared_execution.mimes = "application/json",) -> HARM_Location:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    if new_location.location_id is None:
        logger.debug("• Inserting UUID to location_id")
        new_location.location_id = uuid4()
    with Session(engine) as session:
        stmt = insert(harm_locations)
        stmt = stmt.values(**new_location.model_dump(exclude_unset=True))
        pk = shared_execution.create(stmt=stmt,
                                     session_object=session)
    return get_location(pk_harm_location=pk,
                        output_format=output_format)


# def update_location(update_location: HARM_Location,
#                     output_format: shared_execution.mimes = "application/json",) -> HARM_Location:
#     logger.debug(f"{fa.service}{fa.update} {__name__} {stack()[0][3]}()")
#     with Session(engine) as session:
#         stmt = update(harm_locations)
#         stmt = stmt.where(update_location.location_id)
#         stmt = stmt.values(update_location)
#         execute = session.execute(stmt)
#         commit = session.commit()
#     return get_location(update_location.pk_harm_location)


def delete_location(location_id: UUID,
                    output_format: shared_execution.mimes = "application/json",) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_locations)
        stmt = stmt.where(harm_locations.location_id == location_id)
        shared_execution.delete(stmt=stmt, session_object=session)
    return None


def assign_location_to_record(location_id: UUID, record_hash: str):
    logger.debug(f"{fa.service}{fa.assign} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("Session created")
        stmt = insert(harm_location_to_rec)
        stmt = stmt.values(
            {"fk_harm_location": location_id,
              "fk_data_record": record_hash}
        )
        logger.debug(stmt)
        execute = session.execute(stmt)
        commit = session.commit()
    return None


def remove_location_from_record(location_id: UUID, record_hash: str):
    logger.debug(f"{fa.service}{fa.remove} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_location_to_rec)
        stmt = stmt.where(harm_location_to_rec.fk_data_record == record_hash)
        stmt = stmt.where(
            harm_location_to_rec.fk_harm_location == location_id
        )
        execute = session.execute(stmt)
        commit = session.commit()
    return None

def assign_location_to_dataset(location_id: UUID, dataset_id: UUID):
    logger.debug(f"{fa.service}{fa.assign} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("Session created")
        stmt = insert(harm_location_to_ds)
        stmt = stmt.values(
            {"fk_harm_location": location_id,
              "fk_dataset_id": dataset_id}
        )
        logger.debug(stmt)
        execute = session.execute(stmt)
        commit = session.commit()
    return None


def remove_location_from_dataset(location_id: UUID, dataset_id: UUID):
    logger.debug(f"{fa.service}{fa.remove} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(harm_location_to_ds)
        stmt = stmt.where(harm_location_to_ds.fk_dataset_id == dataset_id)
        stmt = stmt.where(
            harm_location_to_ds.fk_harm_location == location_id
        )
        execute = session.execute(stmt)
        commit = session.commit()
    return None
