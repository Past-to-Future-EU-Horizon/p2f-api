from p2f_api.apilogs import logger, fa
from ..service import harm_timeslice
from p2f_pydantic.harm_timeslices import harm_timeslice as Harm_timeslice
# Third Party Libraries
from fastapi import Body, APIRouter, Request
# Batteries included libraries
import uuid
from typing import Optional, List

router = APIRouter(prefix="/harm-timeslice")

router.get("/")
def list_harm_timeslices(
    named_time_period: Optional[str]=None, 
    older_search_age: Optional[int]=None,
    recent_search_age: Optional[int]=None,
    ) -> List[Harm_timeslice]:
    logger.debug(f"{fa.web}{fa.list} {__name__}")
    return harm_timeslice.list_harm_timeslices(
                    named_time_period=named_time_period,
                    older_search_age=older_search_age,
                    recent_search_age=recent_search_age)

router.get("/")
def get_harm_timeslice(
    timeslice_id: uuid.UUID,
    ) -> Harm_timeslice:
    logger.debug(f"{fa.web}{fa.get} {__name__}")
    return harm_timeslice.get_harm_timeslice(timeslice_id=timeslice_id)

router.post('/')
def create_new_timeslice(
    new_harm_timeslice: Harm_timeslice
    ) -> Harm_timeslice:
    logger.debug(f"{fa.web}{fa.create} {__name__}")
    return harm_timeslice.create_new_timeslice(new_harm_timeslice=new_harm_timeslice)

router.put("/")
def update_timeslice(update_harm_timeslice: Harm_timeslice) -> Harm_timeslice:
    logger.debug(f"{fa.web}{fa.update} {__name__}")
    return harm_timeslice.update_timeslice(update_harm_timeslice=update_harm_timeslice)

router.delete("/{timeslice_id}")
def delete_timeslice(timeslice_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__}")
    return harm_timeslice.delete_timeslice(timeslice_id=timeslice_id)