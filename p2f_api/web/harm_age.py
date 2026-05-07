from p2f_api.apilogs import logger, fa
from ..service import harm_age
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.harm_age import HARM_Rec_Age

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/harm-data-age")

@router.get("/")
def list_harm_ages(
    auth: api_token_annotation,
    recent_year_search: Optional[int] = None,
    older_year_search: Optional[int] = None
) -> List[HARM_Rec_Age]:
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_age.list_harm_ages(
        recent_year_search=recent_year_search,
        older_year_search=older_year_search
    )


@router.get("/{record_hash}")
def get_harm_age(auth: api_token_annotation,
                 record_hash: Optional[str] = None) -> HARM_Rec_Age:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_age.get_harm_age(record_hash=record_hash)


@router.post("/")
def create_new_HARM_Data_Age(auth: api_token_annotation,
                             new_harm_age: HARM_Rec_Age) -> HARM_Rec_Age:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_age.create_new_harm_data_age(new_harm_age=new_harm_age)


@router.put("/", include_in_schema=False)
def update_age(auth: api_token_annotation,
               update_harm_age: HARM_Rec_Age) -> HARM_Rec_Age:
    logger.debug(f"{fa.web}{fa.update} {__name__} {stack()[0][3]}()")
    return harm_age.update_age(update_harm_age=update_harm_age)


@router.delete("/{record_hash}", include_in_schema=False)
def delete_age(auth: api_token_annotation,
               record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_age.delete_age(record_hash=record_hash)
