# Batteries included libraries
from typing import List, Optional
from inspect import stack
from io import BytesIO
import uuid

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from fastapi.responses import Response

# Local libraries
from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.datasets import datasets
from service import shared_execution
from p2f_pydantic.datasets import Datasets

def list_datasets(
    is_new_p2f: Optional[bool] = None,
    is_sub_dataset: Optional[bool] = None,
    doi: Optional[str] = None,
    output_format: shared_execution.mimes = "application/json",
    ) -> List[Datasets] | Response:
    logger.debug(f"{fa.service}{fa.list} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        # logger.debug(f"Parameters: {is_new_p2f}, {is_sub_dataset}, {doi}")
        stmt = select(datasets)
        if is_new_p2f is not None:
            stmt = stmt.where(datasets.is_new_p2f == is_new_p2f)
        if is_sub_dataset is not None:
            stmt = stmt.where(datasets.is_sub_dataset == is_sub_dataset)
        if doi is not None:
            stmt = stmt.where(datasets.doi == doi)
        results = shared_execution.list(stmt=stmt,
                                        pydantic_object=Datasets,
                                        session_object=session,
                                        output_format=output_format)
        logger.debug(f"•  Found {len(results)} results")
    return results


def get_dataset(dataset_id=None,
                output_format: shared_execution.mimes = "application/json", 
                pk_datasets=None) -> Datasets | Response:
    logger.debug(f"{fa.service}{fa.get} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = select(datasets)
        if dataset_id is not None:
            stmt = stmt.where(datasets.dataset_id == dataset_id)
        if pk_datasets is not None:
            stmt = stmt.where(datasets.pk_datasets == pk_datasets)
        result = shared_execution.get(stmt=stmt,
                                      pydantic_object=Datasets,
                                      session_object=session,
                                      output_format=output_format)
    return result


def create_dataset(new_dataset: Datasets,
                   output_format: shared_execution.mimes = "application/json",) -> Datasets:
    logger.debug(f"{fa.service}{fa.create} {stack()[0][3]}()")
    # logger.debug(f"•  received: {new_dataset}")
    if new_dataset.dataset_id is None:
        new_dataset.dataset_id = uuid.uuid4()
    else:
        if get_dataset(dataset_id=new_dataset.dataset_id) is not None:
            new_dataset.dataset_id = uuid.uuid4()
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = insert(datasets)
        stmt = stmt.values(**new_dataset.model_dump(exclude_unset=True))
        logger.debug(f"•  statement: {stmt}")
        inserted_pk = shared_execution.create(stmt=stmt,
                                              session_object=session)
        logger.debug("•  Executed and Commited")
    return get_dataset(pk_datasets=inserted_pk, 
                       output_format=output_format)


def update_dataset(dataset_update: Datasets,
                   output_format: shared_execution.mimes = "application/json",) -> Datasets:
    logger.debug(f"{fa.service}{fa.update} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = update(datasets)
        stmt = stmt.where(
            datasets.dataset_id == dataset_update.dataset_id
        )
        stmt = stmt.values(**dataset_update.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return get_dataset(dataset_id=dataset_update.dataset_id,
                       output_format=output_format)


def delete_dataset(dataset_id,
                   output_format: shared_execution.mimes = "application/json",) -> None:
    logger.debug(f"{fa.service}{fa.delete} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = delete(datasets).where(datasets.dataset_id == dataset_id)
        return shared_execution.delete(stmt=stmt,
                                       session_object=session)
