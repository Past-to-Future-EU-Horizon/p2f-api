# Local libraries
from ..apilogs import logger
from data.db_connection import engine
from data.datasets import datasets
from p2f_pydantic.datasets import Datasets
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List

def list_datasets() -> List[Datasets]:
    """Returns a list of p2f-pydantic Datasets

    Returns:
        Datasets: p2f_pydantic.datasets.Datasets object
    """
    logger.debug("📃 service/datasets.py list_datasets()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(datasets)
        results = session.execute(stmt).all()
        logger.debug(f"\tFound {len(results)} results")
    datasets_list = []
    for result in results:
        datasets_list.append(Datasets(**result[0]))
    return datasets_list

def get_dataset() -> Datasets:
    logger.debug("🔎 service/datasets.py get_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(datasets)

def create_dataset(new_dataset: Datasets) -> Datasets:
    logger.debug("🆕 service/datasets.py create_dataset()")
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
    logger.debug("✏️ service/datasets.py create_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = update(datasets)
        stmt = stmt.where(datasets.pk_datasets == dataset_update.pk_datasets)
        stmt = stmt.values()
        execute = session.execute(stmt)
        commit = session.commit()

def delete_dataset(existing_pk: int) -> None:
    logger.debug("🗑️ service/datasets.py create_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = delete(datasets).where(datasets.pk_datasets == existing_pk)
        execute = session.execute(stmt)
        commit = session.commit()
    return None