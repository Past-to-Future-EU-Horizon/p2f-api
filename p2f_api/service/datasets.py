# Local libraries
from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.datasets import datasets
from p2f_pydantic.datasets import Datasets
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Optional

def list_datasets(
        is_new_p2f: Optional[bool]=None,
        is_sub_dataset: Optional[bool]=None,
        doi: Optional[str]=None
    ) -> List[Datasets]:
    logger.debug(f"{fa.service}{fa.list} service/datasets.py list_datasets()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        # logger.debug(f"Parameters: {is_new_p2f}, {is_sub_dataset}, {doi}")
        stmt = select(datasets)
        if is_new_p2f is not None:
            stmt=stmt.where(datasets.is_new_p2f==is_new_p2f)
        if is_sub_dataset is not None:
            stmt=stmt.where(datasets.is_sub_dataset==is_sub_dataset)
        if doi is not None:
            stmt=stmt.where(datasets.doi==doi)
        results = session.execute(stmt).all()
        logger.debug(f"•  Found {len(results)} results")
    results = [x[0] for x in results]
    datasets_list = [Datasets(**x.__dict__) for x in results]
    return datasets_list

def get_dataset(dataset_id=None,
                pk_datasets=None) -> Datasets:
    logger.debug(f"{fa.service}{fa.get} service/datasets.py get_dataset()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = select(datasets)
        if dataset_id is not None:
            stmt = stmt.where(datasets.dataset_identifier==dataset_id)
        if pk_datasets is not None:
            stmt = stmt.where(datasets.pk_datasets==pk_datasets)
        result = session.execute(stmt).first()
    result = result.tuple()[0]
    ## I hate the current below implementation, but its all I have for now
    return Datasets(**result.__dict__)

def create_dataset(new_dataset: Datasets) -> Datasets:
    logger.debug(f"{fa.service}{fa.create} service/datasets.py create_dataset()")
    logger.debug(f"•  received: {new_dataset}")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = insert(datasets)
        stmt = stmt.values(**new_dataset.model_dump(exclude_unset=True))
        logger.debug(f"•  statement: {stmt}")
        execute = session.execute(stmt)
        commit = session.commit()
        logger.debug("•  Executed and Commited")
    return_dataset = get_dataset(pk_datasets=execute.inserted_primary_key[0])
    return return_dataset

def update_dataset(dataset_update: Datasets) -> Datasets:
    logger.debug(f"{fa.service}{fa.update} service/datasets.py update_dataset()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = update(datasets)
        stmt = stmt.where(datasets.dataset_identifier == dataset_update.dataset_identifier)
        stmt = stmt.values(**dataset_update.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return get_dataset(dataset_id=dataset_update.dataset_identifier)

def delete_dataset(dataset_identifier) -> None:
    logger.debug(f"{fa.service}{fa.delete} service/datasets.py delete_dataset()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = delete(datasets).where(datasets.dataset_identifier == dataset_identifier)
        execute = session.execute(stmt)
        commit = session.commit()
    return None