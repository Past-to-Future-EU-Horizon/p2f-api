# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import datasets
from p2f_pydantic.datasets import Datasets

# Third Party Libraries
from fastapi import Body, APIRouter, Request

# Batteries included libraries
import uuid
from typing import Optional, List
from inspect import stack

router = APIRouter(prefix="/datasets")


# List
@router.get("/")
def list_datasets(
    is_new_p2f: Optional[bool] = None,
    is_sub_dataset: Optional[bool] = None,
    doi: Optional[str] = None,
) -> List[Datasets]:
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    # logger.debug(f"Parameters: {is_new_p2f}, {is_sub_dataset}, {doi}")
    return datasets.list_datasets(
        is_new_p2f=is_new_p2f, is_sub_dataset=is_sub_dataset, doi=doi
    )


# Get Single
@router.get("/{dataset_id}")
def get_dataset(dataset_id) -> Datasets:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return datasets.get_dataset(dataset_id=dataset_id)


# Create
@router.post("/")
def create_dataset(dataset: Datasets) -> Datasets:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return datasets.create_dataset(dataset)


# Update
@router.put("/")
def update_dataset(dataset_updates: Datasets) -> Datasets:
    logger.debug(f"{fa.web}{fa.update} {__name__} {stack()[0][3]}()")
    return datasets.update_dataset(dataset_updates)


# Delete
@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: str) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    if type(dataset_id) == str:
        return datasets.delete_dataset(dataset_id)
