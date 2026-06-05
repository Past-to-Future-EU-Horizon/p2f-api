# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import harm_ds_timecov
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.harm_ds_time import HARM_DS_TimeCoverage
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/time-coverage")

# Get
@router.get("/{dataset_id}")
def get_ds_timecov(auth: api_token_annotation,
                   dataset_id: uuid.UUID) -> HARM_DS_TimeCoverage:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_ds_timecov.get_ds_timecov(dataset_id=dataset_id)

# Create
@router.post("/")
def create_ds_timecov(auth: api_token_annotation,
                      new_timecov: HARM_DS_TimeCoverage) -> HARM_DS_TimeCoverage:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_ds_timecov.create_ds_timecov(new_timecov=new_timecov)

# Delete
@router.delete("/{dataset_id}")
def delete_ds_timecov(auth: api_token_annotation,
                      dataset_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_ds_timecov.delete_ds_timecov(dataset_id=dataset_id)