# Local libraries
from ..apilogs import logger
from ..service import datasets
from p2f_pydantic.datasets import Datasets
# Third Party Libraries
from fastapi import Body, APIRouter, Request
# Batteries included libraries
import uuid
from typing import Optional, List

router = APIRouter(prefix="/datasets")

# List 
@router.get("/")
def list_() -> List[Datasets]:
    return datasets.list_datasets

# Get Single
@router.get("/")
def get_() -> Datasets:
    return datasets.get_dataset

# Create
@router.post("/")
def create_(dataset: Datasets) -> Datasets:
    return datasets.create_dataset(dataset)

# Update 
@router.put("/")
def update_(dataset_updates: Datasets) -> Datasets:
    return datasets.update_dataset(dataset_updates)

# Delete
@router.delete("/")
def delete_(existing_pk: int | Datasets) -> None:
    if type(existing_pk) == int:
        return datasets.delete_dataset(existing_pk)
    elif type(existing_pk) == Datasets:
        return datasets.delete_dataset(existing_pk.pk_datasets)