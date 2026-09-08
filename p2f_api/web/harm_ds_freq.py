# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import harm_ds_freq
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.harm_ds_time import HARM_DS_Frequency
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

tag_name = "Dataset Frequency"

router = APIRouter(prefix="/data-frequency", tags=[tag_name])

tag_metadata = {"name": tag_name,
                "description": 
                """Dataset frequency is a metadata node about how frequent data is within a dataset.

Dataset frequency has the following attributes:
* dataset_id : The unique dataset identifier
* mean_frequency : The mean frequency between data points in a dataset in integer years
* shortest_frequency : The shortest gap between data points in a dataset in integer years [Optional]
* longest_frequency : The longest gap between data points in a dataset in integer years [Optional]"""}

# Get
@router.get("/{dataset_id}", operation_id="datafrequency-get")
def get_ds_freq(auth: api_token_annotation,
                dataset_id: uuid.UUID) -> HARM_DS_Frequency:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_ds_freq.get_ds_freq(dataset_id=dataset_id)

# Create
@router.post("/", operation_id="datafrequency-create")
def create_ds_freq(auth: api_token_annotation,
                   new_frequency: HARM_DS_Frequency) -> HARM_DS_Frequency:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_ds_freq.create_ds_freq(new_frequency=new_frequency)

# Delete
@router.delete("/{dataset_id}", operation_id="datafrequency-delete")
def delete_ds_freq(auth: api_token_annotation,
                   dataset_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_ds_freq.delete_ds_freq(dataset_id=dataset_id)