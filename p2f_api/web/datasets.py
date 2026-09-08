# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import datasets
from .temp_accounts import combined_auth, api_token_annotation, api_token_annotation
from p2f_pydantic.datasets import Datasets
# from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import APIRouter, Security, Depends
from fastapi import Header, Body

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/datasets", tags=["Datasets"])


# List
@router.get("/", operation_id="dataset-list")
def list_datasets(
    auth: api_token_annotation,
    is_new_p2f: Optional[bool] = None,
    is_sub_dataset: Optional[bool] = None,
    doi: Optional[str] = None,
) -> List[Datasets]:
    """List the datasets available on the API

    Args:
        auth (api_token_annotation): _description_
        is_new_p2f (Optional[bool], optional): Is the dataset a product of the P2F project (True) or created prior (False). Defaults to None.
        is_sub_dataset (Optional[bool], optional): Is the dataset a part of a larger dataset?. Defaults to None.
        doi (Optional[str], optional): The digital object identifier of a dataset. Defaults to None.

    Returns:
        List[Datasets]: A list of the datasets that meet the search criteria
    """
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    # logger.debug(f"Parameters: {is_new_p2f}, {is_sub_dataset}, {doi}")
    return datasets.list_datasets(
        is_new_p2f=is_new_p2f, is_sub_dataset=is_sub_dataset, doi=doi
    )


# Get Single
@router.get("/{dataset_id}", operation_id="dataset-get")
def get_dataset(auth: api_token_annotation,
                dataset_id: uuid.UUID) -> Datasets:
    """Get an individual dataset by its dataset_id

    Args:
        auth (api_token_annotation): _description_
        dataset_id (uuid.UUID): _description_

    Returns:
        Datasets: A single p2f-pydantic dataset object
    """
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return datasets.get_dataset(dataset_id=dataset_id)


# Create
@router.post("/", operation_id="dataset-create")
def create_dataset(auth: api_token_annotation,
                   dataset: Datasets) -> Datasets:
    """Create a new dataset record on the API with a p2f-pydantic Datasets object

    Args:
        auth (api_token_annotation): _description_
        dataset (Datasets): The new p2f-pydantic Datasets object

    Returns:
        Datasets: The resulting ingestion of the new dataset in the API
    """     
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return datasets.create_dataset(dataset)


# Update
@router.put("/", include_in_schema=False, operation_id="dataset-update")
def update_dataset(auth: api_token_annotation,
                   dataset_updates: Datasets) -> Datasets:
    """Update a dataset on the API using a p2f-pydantic Datasets object

    Args:
        auth (api_token_annotation): _description_
        dataset_updates (Datasets): The updated p2f-pydantic Datasets object, the dataset_id must be set. 

    Returns:
        Datasets: The resulting updated p2f-pydantic Datasets object from the API. 
    """
    logger.debug(f"{fa.web}{fa.update} {__name__} {stack()[0][3]}()")
    return datasets.update_dataset(dataset_updates)


# Delete
@router.delete("/{dataset_id}", include_in_schema=False, operation_id="dataset-delete")
def delete_dataset(auth: api_token_annotation,
                   dataset_id: uuid.UUID) -> None:
    """Delete a dataset from the portal. 

    Args:
        auth (api_token_annotation): _description_
        dataset_id (uuid.UUID): The unique identifier of the dataset
    """
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    if type(dataset_id) == str:
        return datasets.delete_dataset(dataset_id)
