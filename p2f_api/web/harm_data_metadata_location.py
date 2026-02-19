# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import harm_data_metadata_location
from p2f_pydantic.harm_data_metadata import harm_location as Harm_location
from p2f_pydantic.harm_data_metadata import harm_bounding_box as Harm_bounding_box

# Third Party Libraries
from fastapi import Body, APIRouter, Request

# Batteries included libraries
import uuid
from typing import Optional, List
from inspect import stack

router = APIRouter(prefix="/harm-data-locations")


# List
@router.get("/")
def list_harm_data_records(
    bounding_box: Optional[Harm_bounding_box] = None,
    location_name: Optional[str] = None,
    location_code: Optional[str] = None,
    minimum_elevation: Optional[float] = None,
    maximum_elevation: Optional[float] = None,
    min_location_age: Optional[float] = None,
    max_location_age: Optional[float] = None,
    dataset_id: Optional[uuid.UUID] = None,
) -> List[Harm_location]:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_data_metadata_location.list_harm_metadata_location(
        bounding_box=bounding_box,
        location_name=location_name,
        location_code=location_code,
        minimum_elevation=minimum_elevation,
        maximum_elevation=maximum_elevation,
        min_location_age=min_location_age,
        max_location_age=max_location_age,
        dataset_id=dataset_id,
    )


# Get Single
@router.get("/{location_identifier}")
def get_harm_data_record(location_identifier: uuid.UUID) -> Harm_location:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_data_metadata_location.get_location(
        location_identifier=location_identifier
    )


# Create
@router.post("/")
def create_dataset(new_location: Harm_location) -> Harm_location:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_data_metadata_location.create_location(new_location=new_location)


@router.put("/")
def update_dataset(update_location: Harm_location) -> Harm_location:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_data_metadata_location.update_location(update_location=update_location)


# Delete
@router.delete("/{location_identifier}")
def delete_dataset(location_identifier: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_data_metadata_location.delete_location(
        location_identifier=location_identifier
    )


@router.post("/assign")
def assign_location_to_record(location_identifier: uuid.UUID, record_hash: str):
    logger.debug(
        f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}({location_identifier}, {record_hash})"
    )
    return harm_data_metadata_location.assign_location_to_record(
        location_identifier=location_identifier, record_hash=record_hash
    )


@router.delete("/remove")
def remove_location_from_record(location_identifier: uuid.UUID, record_hash: str):
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_data_metadata_location.remove_location_from_record(
        location_identifier=location_identifier, record_hash=record_hash
    )
