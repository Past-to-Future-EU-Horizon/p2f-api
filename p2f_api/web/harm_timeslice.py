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

router = APIRouter(prefix="/harm-timeslice")


@router.get("/")
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


@router.get("/")
def get_harm_timeslice(
    auth: api_token_annotation,
    timeslice_id: uuid.UUID,
) -> HARM_Timeslice:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_timeslice.get_harm_timeslice(timeslice_id=timeslice_id)


@router.post("/")
def create_new_timeslice(auth: api_token_annotation,
                         new_harm_timeslice: HARM_Timeslice) -> HARM_Timeslice:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_timeslice.create_new_timeslice(new_harm_timeslice=new_harm_timeslice)


@router.put("/", include_in_schema=False)
def update_timeslice(auth: api_token_annotation,
                     update_harm_timeslice: HARM_Timeslice) -> HARM_Timeslice:
    logger.debug(f"{fa.web}{fa.update} {__name__} {stack()[0][3]}()")
    return harm_timeslice.update_timeslice(update_harm_timeslice=update_harm_timeslice)


@router.delete("/{timeslice_id}", include_in_schema=False)
def delete_timeslice(auth: api_token_annotation,
                     timeslice_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_timeslice.delete_timeslice(timeslice_id=timeslice_id)


@router.post("/assign")
def assign_timeslice(auth: api_token_annotation,
                     timeslice_id: uuid.UUID, record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_timeslice.assign_timeslice(
        timeslice_id=timeslice_id, record_hash=record_hash
    )


@router.delete("/remove")
def remove_timeslice(auth: api_token_annotation,
                     timeslice_id: uuid.UUID, record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_timeslice.remove_timeslice(
        timeslice_id=timeslice_id, record_hash=record_hash
    )
