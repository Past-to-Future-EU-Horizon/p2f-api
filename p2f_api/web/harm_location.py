# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import harm_locations
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.harm_location import HARM_Location
from p2f_pydantic.harm_location import HARM_Bounding_Box
from p2f_pydantic.temp_accounts import Temp_Account
# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/harm-data-locations")


# List
@router.get("/")
def list_harm_data_records(
    auth: api_token_annotation,
    bounding_box: Optional[HARM_Bounding_Box] = None,
    location_name: Optional[str] = None,
    location_code: Optional[str] = None,
    minimum_elevation: Optional[float] = None,
    maximum_elevation: Optional[float] = None,
    min_location_age: Optional[float] = None,
    max_location_age: Optional[float] = None,
    dataset_id: Optional[uuid.UUID] = None,
) -> List[HARM_Location]:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_locations.list_harm_metadata_location(
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
@router.get("/{location_id}")
def get_harm_data_record(auth: api_token_annotation,
                         location_id: uuid.UUID) -> HARM_Location:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_locations.get_location(
        location_id=location_id
    )


# Create
@router.post("/")
def create_dataset(auth: api_token_annotation,
                   new_location: HARM_Location) -> HARM_Location:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_locations.create_location(new_location=new_location)


@router.put("/", include_in_schema=False)
def update_dataset(auth: api_token_annotation,
                   update_location: HARM_Location) -> HARM_Location:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_locations.update_location(update_location=update_location)


# Delete
@router.delete("/{location_id}", include_in_schema=False)
def delete_dataset(auth: api_token_annotation,
                   location_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_locations.delete_location(
        location_id=location_id
    )


@router.post("/assign")
def assign_location_to_record(auth: api_token_annotation,
                              location_id: uuid.UUID, record_hash: str):
    logger.debug(
        f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}({location_id}, {record_hash})"
    )
    return harm_locations.assign_location_to_record(
        location_id=location_id, record_hash=record_hash
    )


@router.delete("/remove")
def remove_location_from_record(auth: api_token_annotation,
                                location_id: uuid.UUID, record_hash: str):
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_locations.remove_location_from_record(
        location_id=location_id, record_hash=record_hash
    )
