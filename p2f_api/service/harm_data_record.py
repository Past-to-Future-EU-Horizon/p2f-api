# Local libraries
from p2f_api.apilogs import logger
# from ..service.harm_numerical import list_numerics
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
        # data_type: Optional[int]=None,  ## Disabling this for now
                                          ## I would need to duplicate the code in the numerical service
                                          ## as this is currently causing circular import issues. 
                    ) -> List[Harm_data_record]:
    logger.debug("📃 service/harm_data_record.py list_harm_data_record()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(harm_data_record)
        if dataset is not None:
            stmt = stmt.where(harm_data_record.fk_dataset == dataset)
        # if data_type is not None: ### Disabled
        #     subqry = (select().subquery())
        results = session.execute(stmt).all()
        logger.debug(f"\tFound {len(results)} results")
    return [Harm_data_record(**x[0].__dict__) for x in results]

def get_harm_data_record(record_hash: Optional[str]=None,
                         pk_harm_data_record: Optional[int]=None) -> Harm_data_record:
    logger.debug("🔎 service/harm_data_record.py get_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(harm_data_record)
        if record_hash is not None:
            stmt = stmt.where(harm_data_record.record_hash == record_hash)
        if pk_harm_data_record is not None:
            stmt = stmt.where(harm_data_record.pk_harm_data_record==pk_harm_data_record)
        result = session.execute(stmt).first()
    return Harm_data_record(**result.tuple()[0].__dict__)

def create_harm_data_record(new_dataset: Harm_data_record) -> Harm_data_record:
    logger.debug("🆕 service/harm_data_record.py create_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = insert(harm_data_record)
        stmt = stmt.values(**new_dataset.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return get_harm_data_record(pk_harm_data_record=execute.inserted_primary_key[0])

def update_harm_data_record(record_hash:str, 
                            dataset_update: Harm_data_record) -> Harm_data_record:
    logger.debug("✏️ service/harm_data_record.py create_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = update(harm_data_record)
        stmt = stmt.where(harm_data_record.pk_harm_data_record == dataset_update.pk_harm_data_record)
        stmt = stmt.values()
        execute = session.execute(stmt)
        commit = session.commit()
    return get_harm_data_record(pk_harm_data_record=dataset_update.pk_harm_data_record)

def delete_harm_data_record(record_hash: str) -> None:
    logger.debug("🗑️ service/harm_data_record.py create_dataset()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = delete(harm_data_record).where(harm_data_record.record_hash == record_hash)
        execute = session.execute(stmt)
        commit = session.commit()
    return None