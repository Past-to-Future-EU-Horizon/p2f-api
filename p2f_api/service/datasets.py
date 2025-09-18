# Local libraries
from ..apilogs import logger
from data.db_connection import engine
from data.datasets import datasets
from p2f_pydantic.datasets import Datasets
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Optional

def list_datasets(
        is_new_p2f: Optional[bool]=None,
        is_sub_dataset: Optional[bool]=None
    ) -> List[Datasets]:
    logger.debug("💾📃 service/datasets.py list_datasets()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(datasets)
        results = session.execute(stmt).all()
        logger.debug(f"\tFound {len(results)} results")
    datasets_list = []
    for result in results:
        datasets_list.append(Datasets(**result[0]))
    return datasets_list

def get_dataset(dataset_id) -> Datasets:
    logger.debug("💾🔎 service/datasets.py get_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(datasets)
        stmt = stmt.where(datasets.dataset_identifier==dataset_id)
        result = session.execute(stmt)
        if len(result) == 1:
            return Datasets(**result[0].tuple())

def create_dataset(new_dataset: Datasets) -> Datasets:
    logger.debug("💾🆕 service/datasets.py create_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = insert(datasets)
        stmt = stmt.values()
        execute = session.execute(stmt)
        commit = session.commit()
    return_dataset = new_dataset
    return_dataset.pk_datasets = execute.inserted_primary_key
    return return_dataset

def update_dataset(dataset_update: Datasets) -> Datasets:
    logger.debug("💾✏️ service/datasets.py update_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = update(datasets)
        stmt = stmt.where(datasets.dataset_identifier == dataset_update.dataset_identifier)
        stmt = stmt.values()
        execute = session.execute(stmt)
        commit = session.commit()

def delete_dataset(existing_pk: int) -> None:
    logger.debug("💾🗑️ service/datasets.py delete_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = delete(datasets).where(datasets.pk_datasets == existing_pk)
        execute = session.execute(stmt)
        commit = session.commit()
    return None