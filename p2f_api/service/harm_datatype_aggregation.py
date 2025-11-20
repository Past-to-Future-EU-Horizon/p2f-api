# Local libraries
from p2f_api.apilogs import logger
from data.harm_data_types import harm_data_type
from data.datasets import datasets
from data.harm_data_numerical import harmonized_float, harmonized_float_confidence
from data.harm_data_numerical import harmonized_int, harmonized_int_confidence
from data.harm_data_record import harm_data_record
from data.db_connection import engine
from service import datasets as service_datasets
from p2f_pydantic.datasets import Datasets
# Third Party Libraries
from sqlalchemy import select, join
from sqlalchemy.orm import Session
# Batteries included libraries
from uuid import UUID
from typing import List

def get_datasets_by_data_type_APISIDE(datatype_id: UUID) -> List[UUID]:
    # Select unique record hashes from numerical types where datatype == datatype_id
    # Select unique datasets from above record hashes
    with Session(engine) as session:
        # Subquery harmonized int
        sq_hi = select(harmonized_int.fk_data_record)
        sq_hi = sq_hi.where(harmonized_int.fk_data_type==datatype_id)
        # Subquery harmonized int confidence
        sq_hic = select(harmonized_int_confidence.fk_data_record)
        sq_hic = sq_hic.where(harmonized_int_confidence.fk_data_type == datatype_id)
        # Subquery harmonized float
        sq_hf = select(harmonized_float.fk_data_record)
        sq_hf = sq_hf.where(harmonized_float.fk_data_type==datatype_id)
        # Subquery harmonized float confidence
        sq_hfc = select(harmonized_float_confidence.fk_data_record)
        sq_hfc = sq_hfc.where(harmonized_float_confidence.fk_data_type == datatype_id)
        # Execute above subqueries
        ru_hi = session.execute(sq_hi).unique()
        ru_hic = session.execute(sq_hic).unique()
        ru_hf = session.execute(sq_hf).unique()
        ru_hfc = session.execute(sq_hfc).unique()
        # Process results objects into lists
        ru_hi = [x[0] for x in ru_hi]
        ru_hic = [x[0] for x in ru_hic]
        ru_hf = [x[0] for x in ru_hf]
        ru_hfc = [x[0] for x in ru_hfc]
        # Bring the lists together
        ru = ru_hi + ru_hic + ru_hf + ru_hfc
        # Simple Unique function to get the unique record hashes
        ru = list(set(ru))
        query = select(harm_data_record.fk_dataset)
        query = query.where(harm_data_record.record_hash.in_(ru))
        execute = session.execute(query).unique()
        return [x[0] for x in execute]

def get_datasets_by_data_type_POSTGRESIDE(datatype_id: UUID) -> List[UUID]:
    with Session(engine) as session:
        sq_hi = (select(harmonized_int.fk_data_record)
                 .where(harmonized_int.fk_data_type==datatype_id)
                 .distinct().subquery())
        tq_hi = select(harm_data_record.fk_dataset)
        tq_hi = tq_hi.where(harm_data_record.record_hash.in_(sq_hi.c.fk_data_record))
        logger.debug(f"harmonized int Select statement with Subquery: \n{tq_hi}")
        ex_hi = session.execute(tq_hi).unique()
        sq_hic = (select(harmonized_int.fk_data_record)
                 .where(harmonized_int.fk_data_type==datatype_id)
                 .distinct().subquery())
        tq_hic = select(harm_data_record.fk_dataset)
        tq_hic = tq_hic.where(harm_data_record.record_hash.in_(sq_hic.c.fk_data_record))
        logger.debug(f"harmonized int confidence Select statement with Subquery: \n{tq_hic}")
        ex_hic = session.execute(tq_hic).unique()
        sq_hf = (select(harmonized_int.fk_data_record)
                 .where(harmonized_int.fk_data_type==datatype_id)
                 .distinct().subquery())
        tq_hf = select(harm_data_record.fk_dataset)
        tq_hf = tq_hf.where(harm_data_record.record_hash.in_(sq_hf.c.fk_data_record))
        logger.debug(f"harmonized float Select statement with Subquery: \n{tq_hf}")
        ex_hf = session.execute(tq_hf).unique()
        sq_hfc = (select(harmonized_int.fk_data_record)
                 .where(harmonized_int.fk_data_type==datatype_id)
                 .distinct().subquery())
        tq_hfc = select(harm_data_record.fk_dataset)
        tq_hfc = tq_hfc.where(harm_data_record.record_hash.in_(sq_hfc.c.fk_data_record))
        logger.debug(f"harmonized float confidence Select statement with Subquery: \n{tq_hfc}")
        ex_hfc = session.execute(tq_hfc).unique()
        ex_hi = [x[0] for x in ex_hi]
        ex_hic = [x[0] for x in ex_hic]
        ex_hf = [x[0] for x in ex_hf]
        ex_hfc = [x[0] for x in ex_hfc]
        ex_all = ex_hi + ex_hic + ex_hf + ex_hfc
        return ex_all
    
def get_dataset_objs_by_datatype_id(datatype_id: UUID) -> List[Datasets]:
    dataset_ids = get_datasets_by_data_type_POSTGRESIDE(datatype_id=datatype_id)
    return [service_datasets.get_dataset(dataset_id=x) for x in dataset_ids]