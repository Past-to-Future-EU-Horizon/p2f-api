from p2f_api.apilogs import logger, fa
from ..service import harm_timeslice
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.harm_timeslices import HARM_Timeslice
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

tag_name = "HARM Timeslice"

router = APIRouter(prefix="/harm-timeslice", tags=[tag_name])

tag_metadata = {"name": tag_name,
                "description": 
                """The Past 2 Future project has created named timeslices to refer to specific time periods, this metadata node will associate timeslices with datasets and data records. 

HARM Timeslices have the following attributes:

* timeslice_id : A unique identifier for the timeslice in the UUID format, this is created by the server, do not create this yourself. 
* timeslice_name : The name created by the Past 2 Future Project
* timeslice_age_mean : The central year used to describe a timeslice or time event
* timeslice_age_recent : The most recent year to describe a timeslice as a range
* timeslice_age_oldest : The older year to describe a timeslice as a range"""}

@router.get("/", operation_id="timeslice-list")
def list_harm_timeslices(
    auth: api_token_annotation,
    named_time_period: Optional[str] = None,
    older_search_age: Optional[int] = None,
    recent_search_age: Optional[int] = None,
) -> List[HARM_Timeslice]:
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    return harm_timeslice.list_harm_timeslices(
        named_time_period=named_time_period,
        older_search_age=older_search_age,
        recent_search_age=recent_search_age,
    )


@router.get("/", operation_id="timeslice-get")
def get_harm_timeslice(
    auth: api_token_annotation,
    timeslice_id: uuid.UUID,
) -> HARM_Timeslice:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_timeslice.get_harm_timeslice(timeslice_id=timeslice_id)


@router.post("/", operation_id="timeslice-create")
def create_new_timeslice(auth: api_token_annotation,
                         new_harm_timeslice: HARM_Timeslice) -> HARM_Timeslice:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_timeslice.create_new_timeslice(new_harm_timeslice=new_harm_timeslice)


@router.put("/", include_in_schema=False, operation_id="timeslice-update")
def update_timeslice(auth: api_token_annotation,
                     update_harm_timeslice: HARM_Timeslice) -> HARM_Timeslice:
    logger.debug(f"{fa.web}{fa.update} {__name__} {stack()[0][3]}()")
    return harm_timeslice.update_timeslice(update_harm_timeslice=update_harm_timeslice)


@router.delete("/{timeslice_id}", include_in_schema=False, operation_id="timeslice-delete")
def delete_timeslice(auth: api_token_annotation,
                     timeslice_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_timeslice.delete_timeslice(timeslice_id=timeslice_id)


@router.post("/assign", operation_id="timeslice_recordhash-assign")
def assign_timeslice(auth: api_token_annotation,
                     timeslice_id: uuid.UUID, record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_timeslice.assign_timeslice(
        timeslice_id=timeslice_id, record_hash=record_hash
    )


@router.delete("/remove", operation_id="timeslice_recordhash-remove")
def remove_timeslice(auth: api_token_annotation,
                     timeslice_id: uuid.UUID, record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_timeslice.remove_timeslice(
        timeslice_id=timeslice_id, record_hash=record_hash
    )
