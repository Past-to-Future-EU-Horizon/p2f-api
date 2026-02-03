from p2f_api.apilogs import logger, fa
from ..service import harm_age
from p2f_pydantic.harm_age import harm_data_age as Harm_data_age
# Third Party Libraries
from fastapi import Body, APIRouter, Request
# Batteries included libraries
import uuid
from typing import Optional, List

router = APIRouter(prefix="/harm-data-age")

router.get("/")
def list_harm_ages(recent_year_search: Optional[int]=None, 
                   older_year_search: Optional[int]=None) -> List[Harm_data_age]:
    logger.debug(f"{fa.web}{fa.list} {__name__}")
    return harm_age.list_harm_ages(recent_year_search=recent_year_search,
                                   older_year_search=older_year_search)

router.get("/{record_hash}")
def get_harm_age(
    record_hash: Optional[str]=None
    ) -> Harm_data_age:
    logger.debug(f"{fa.web}{fa.get} {__name__}")
    return harm_age.get_harm_age(record_hash=record_hash)

router.post('/')
def create_new_harm_data_age(
    new_harm_age: Harm_data_age
    ) -> Harm_data_age:
    logger.debug(f"{fa.web}{fa.create} {__name__}")
    return harm_age.create_new_harm_data_age(new_harm_age=new_harm_age)

router.put("/")
def update_age(update_harm_age: Harm_data_age) -> Harm_data_age:
    logger.debug(f"{fa.web}{fa.update} {__name__}")
    return harm_age.update_age(update_harm_age=update_harm_age)

router.delete("/{record_hash}")
def delete_age(record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__}")
    return harm_age.delete_age(record_hash=record_hash)