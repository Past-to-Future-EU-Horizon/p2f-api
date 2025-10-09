# Local libraries
from ..apilogs import logger
from ..service.harm_numerical import list_numerics
from ..data.db_connection import engine
from ..data.harm_data_record import harm_data_record
from p2f_pydantic.harm_data_record import harm_data_record as Harm_data_record
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Optional
from uuid import UUID

def list_harm_data_record(
        dataset: Optional[UUID]=None, 
        data_type: Optional[int]=None,  ## LOL TODO this is gonna be rough
                    ) -> List[Harm_data_record]:
    logger.debug("📃 service/harm_data_record.py list_harm_data_record()")
    if data_type:
        #! This may not be the most SQL way to do this search, there may be a better way with ForeignKey relations
        ## Currently implemented this method using the service from the service.harm_numerical module
        ## The list comprehension will get the data record IDs for the matching data types
        ## the list(set()) run on the list comprehension will produce a list of unique values
        matching_numerics = list(set([x.fk_data_record for x in list_numerics(data_type=data_type)]))
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(harm_data_record)
        results = session.execute(stmt).all()
        logger.debug(f"\tFound {len(results)} results")
    harm_data_record_list = []
    for result in results:
        harm_data_record_list.append(Harm_data_record(**result[0]))
    return harm_data_record_list

def get_harm_data_record(record_hash: str) -> Harm_data_record:
    logger.debug("🔎 service/harm_data_record.py get_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(harm_data_record)
        stmt = stmt.where(harm_data_record.record_hash == record_hash)
        result = session.execute(stmt)
        if len(result) == 1:
            return Harm_data_record(**result[0].tuple())

def create_harm_data_record(new_dataset: Harm_data_record) -> Harm_data_record:
    logger.debug("🆕 service/harm_data_record.py create_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = insert(harm_data_record)
        stmt = stmt.values()
        execute = session.execute(stmt)
        commit = session.commit()
    return_dataset = new_dataset
    return_dataset.pk_harm_data_record = execute.inserted_primary_key
    return return_dataset

def update_harm_data_record(dataset_update: Harm_data_record) -> Harm_data_record:
    logger.debug("✏️ service/harm_data_record.py create_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = update(harm_data_record)
        stmt = stmt.where(harm_data_record.pk_harm_data_record == dataset_update.pk_harm_data_record)
        stmt = stmt.values()
        execute = session.execute(stmt)
        commit = session.commit()

def delete_harm_data_record(record_hash: str) -> None:
    logger.debug("🗑️ service/harm_data_record.py create_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = delete(harm_data_record).where(harm_data_record.pk_harm_data_record == record_hash)
        execute = session.execute(stmt)
        commit = session.commit()
    return None