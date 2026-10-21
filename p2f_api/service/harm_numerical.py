# Batteries included libraries
from typing import List, Union, Literal, Optional
from uuid import UUID
from inspect import stack

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from sqlalchemy import func
import pandas as pd

# Local libraries
from p2f_api.apilogs import logger, fa
from service import shared_execution
from .harm_data_record import list_harm_data_record
from .datasets import get_dataset, list_datasets
from ..data.db_connection import engine
from ..data.harm_data_numerical import harmonized_float_confidence, harmonized_float
from ..data.harm_data_numerical import harmonized_int_confidence, harmonized_int
from ..data.harm_data_numerical import harmonized_numeric_id_map
from ..data.harm_data_record import harm_data_record
from p2f_pydantic.harm_data_numerical import HARM_Int, HARM_Int_Confidence
from p2f_pydantic.harm_data_numerical import HARM_Float, HARM_Float_Confidence
from p2f_pydantic.harm_data_numerical import Insert_HARM_Numerical, Return_HARM_Numerical
from p2f_pydantic.harm_data_numerical import Numerical_Table_Statistics


Harm_numerical_union = Union[HARM_Int, HARM_Int_Confidence, HARM_Float, HARM_Float_Confidence]

harm_table_matching = {
    "float_confidence": {
        "db": harmonized_float_confidence,
        "pydantic": HARM_Float_Confidence,
    },
    "float": {
        "db": harmonized_float, 
        "pydantic": HARM_Float
    },
    "int_confidence": {
        "db": harmonized_int_confidence,
        "pydantic": HARM_Int_Confidence,
    },
    "int": {
        "db": harmonized_int, 
        "pydantic": HARM_Int
    },
    "float_confidence".upper(): {
        "db": harmonized_float_confidence,
        "pydantic": HARM_Float_Confidence,
    },
    "float".upper(): {
        "db": harmonized_float, 
        "pydantic": HARM_Float
    },
    "int_confidence".upper(): {
        "db": harmonized_int_confidence,
        "pydantic": HARM_Int_Confidence,
    },
    "int".upper(): {
        "db": harmonized_int, 
        "pydantic": HARM_Int
    }
}


def get_numeric_types_stats(datatype_id: UUID | None = None,
                            dataset_id: UUID | None = None,
                            record_hash: str | None = None) -> Numerical_Table_Statistics: 
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt_int = select(func.count()).select_from(harmonized_int)
        stmt_intc = select(func.count()).select_from(harmonized_int_confidence)
        stmt_float = select(func.count()).select_from(harmonized_float)
        stmt_floatc = select(func.count()).select_from(harmonized_float_confidence)
    if datatype_id is not None:
        stmt_int = stmt_int.where(harmonized_int.fk_data_type == datatype_id)
        stmt_intc = stmt_intc.where(harmonized_int_confidence.fk_data_type == datatype_id)
        stmt_float = stmt_float.where(harmonized_float.fk_data_type == datatype_id)
        stmt_floatc = stmt_floatc.where(harmonized_float_confidence.fk_data_type == datatype_id)
    if dataset_id is not None:
        # Was experiencing an error on only float confidence with a shared subquery. Therefore all get their own subquery.
        sbqr_dataset_int = select(harm_data_record.record_hash.distinct()).where(harm_data_record.fk_dataset == dataset_id)
        sbqr_dataset_intc = select(harm_data_record.record_hash.distinct()).where(harm_data_record.fk_dataset == dataset_id)
        sbqr_dataset_float = select(harm_data_record.record_hash.distinct()).where(harm_data_record.fk_dataset == dataset_id)
        sbqr_dataset_floatc = select(harm_data_record.record_hash.distinct()).where(harm_data_record.fk_dataset == dataset_id)
        stmt_int = stmt_int.where(harmonized_int.fk_data_record.in_(sbqr_dataset_int))
        stmt_intc = stmt_intc.where(harmonized_int_confidence.fk_data_record.in_(sbqr_dataset_intc))
        stmt_float = stmt_float.where(harmonized_float.fk_data_record.in_(sbqr_dataset_float))
        stmt_floatc = stmt_floatc.where(harmonized_float_confidence.fk_data_record.in_(sbqr_dataset_floatc))
    if record_hash is not None:
        stmt_int = stmt_int.where(harmonized_int.fk_data_record == record_hash)
        stmt_intc = stmt_intc.where(harmonized_int_confidence.fk_data_record == record_hash)
        stmt_float = stmt_float.where(harmonized_float.fk_data_record == record_hash)
        stmt_floatc = stmt_floatc.where(harmonized_float_confidence.fk_data_record == record_hash)
    # logger.debug(f"=============Statments for counts==========\nInt: {stmt_int}\n\nIntConf: {stmt_intc}\n\nFloat: {stmt_float}\n\nFloatConf: {stmt_floatc}\n=============")
    result_int = session.execute(stmt_int).first()
    result_intc = session.execute(stmt_intc).first()
    result_float = session.execute(stmt_float).first()
    result_floatc = session.execute(stmt_floatc).first()
    # logger.debug(f"==========Results===============\nInt: {result_int[0]}\nIntConf: {result_intc[0]}\nFloat: {result_float[0]}\nFloatConf: {result_floatc[0]}")
    return Numerical_Table_Statistics(count_int=result_int[0],
                                      count_int_confidence=result_intc[0],
                                      count_float=result_float[0],
                                      count_float_confidence=result_floatc[0])
            

def get_numeric_table_by_uuid(numeric_id: UUID):
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        logger.debug("•  Created session")
        stmt = select(harmonized_numeric_id_map)
        stmt = stmt.where(harmonized_numeric_id_map.fk_harm_num == numeric_id)
        result = session.execute(stmt).first()
    # logger.debug(dir())
    numeric_class = result.tuple()[0].table_class
    logger.debug(f"•• Numeric Class set as {numeric_class}")
    numeric_table = harm_table_matching[numeric_class]["db"]
    pydantic_class = harm_table_matching[numeric_class]["pydantic"]
    return (numeric_table, pydantic_class)

def list_numerics_single_type(
        numeric_type: Literal["float_confidence", "float", "int_confidence", "int",
                              "FLOAT_CONFIDENCE", "FLOAT", "INT_CONFIDENCE", "INT"], # Now required, iterate elsewhere
        record_hash: Optional[str] = None,
        datatype_id: Optional[UUID] = None,
        dataset_id: Optional[UUID] = None,
        output_format: shared_execution.mimes = "application/json",
    ): # -> Return only one kind of table 
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}({numeric_type})")
    TABLE, PYDANTIC = harm_table_matching[numeric_type]["db"], harm_table_matching[numeric_type]["pydantic"]
    ########### The following code block has many time out errors due to the complexity of the search.
    # if dataset_id is not None:
    #     # Gather information on the dataset. 
    #     ##  If its a parent dataset, get the children, otherwise just collect exactly that dataset 
    #     logger.debug("•  dataset_id is not none")
    #     dataset_filter = get_dataset(dataset_id=dataset_id)
    #     if not dataset_filter.is_sub_dataset:
    #         related_datasets = list_datasets(doi=dataset_filter.doi)
    #         related_dataset_ids = [x.dataset_id for x in related_datasets]
    #     else:
    #         related_datasets = [dataset_filter]
    #         related_dataset_ids = [dataset_filter.dataset_id]
    with Session(engine) as session:
        stmt = select(TABLE)
        if record_hash is not None:
            logger.debug(f"•• record_hash is not None {record_hash}")
            stmt = stmt.where(TABLE.fk_data_record == record_hash)
        if datatype_id is not None:
            logger.debug(f"•• datatype_id is not None {datatype_id}")
            stmt = stmt.where(TABLE.fk_data_type == datatype_id)
        if dataset_id is not None:
            logger.debug(f"•• dataset_id is not None {dataset_id}")
            # What we want here are all the record hashes under a dataset
            subqry = select(harm_data_record.record_hash.distinct())
            subqry = subqry.where(harm_data_record.fk_dataset == dataset_id)
            stmt = stmt.where(TABLE.fk_data_record.in_(subqry))
        results = shared_execution.list(stmt=stmt,
                                        pydantic_object=PYDANTIC,
                                        session_object=session,
                                        output_format=output_format)
    return results
        
def list_numerics_type_iterator(
        record_hash: Optional[str] = None,
        datatype_id: Optional[UUID] = None,
        dataset_id: Optional[UUID] = None,
        output_format: shared_execution.mimes = "application/json",
    ) -> Return_HARM_Numerical:
    stats = None
    numeric_type_iteration = ["float_confidence", "float", "int_confidence", "int"]
    if datatype_id is not None or dataset_id is not None or record_hash is not None:
        stats = get_numeric_types_stats(dataset_id=dataset_id, datatype_id=datatype_id, record_hash=record_hash).model_dump(exclude_unset=True)
        # logger.debug(f"stats dictionary before comprehension: {stats}")
        stats = {x.replace("count_", ""): y for x, y in stats.items() if y > 0}
        # logger.debug(f"stats dictionary after comprehension: {stats}")
        numeric_type_iteration = [x for x in numeric_type_iteration if x in stats.keys()]
    results = {}
    logger.debug(f"numeric types to iterate: {numeric_type_iteration}")
    for numeric_type in numeric_type_iteration:
        if output_format == "application/json":
            iteration_results = list_numerics_single_type(numeric_type=numeric_type,
                                                          record_hash=record_hash,
                                                          datatype_id=datatype_id,
                                                          dataset_id=dataset_id, 
                                                          output_format=output_format)
            results[numeric_type] = iteration_results
    results = {f"data_harmonized_{x}": y for x, y in results.items()}
    results = Return_HARM_Numerical(**results)
    return results
    
def get_numeric(numeric_id: UUID) -> Harm_numerical_union:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    numeric_table, pydantic_class = get_numeric_table_by_uuid(numeric_id=numeric_id)
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(numeric_table)
        stmt = stmt.where(numeric_table.pk_harm_num == numeric_id)
        result = session.execute(stmt).first()
    numeric_object = pydantic_class(**result.tuple()[0].__dict__)
    return numeric_object


def create_numeric(new_numeric: Insert_HARM_Numerical) -> Insert_HARM_Numerical:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    numeric_class = new_numeric.numerical_type
    if numeric_class == "INT":
        if new_numeric.upper_conf_value and new_numeric.lower_conf_value:
            numeric_class = numeric_class + "_CONFIDENCE"
            numerical_table = harmonized_int_confidence
        else:
            numerical_table = harmonized_int
    elif numeric_class == "FLOAT":
        if new_numeric.upper_conf_value and new_numeric.lower_conf_value:
            numeric_class = numeric_class + "_CONFIDENCE"
            numerical_table = harmonized_float_confidence
        else:
            numerical_table = harmonized_float
    else:
        raise ValueError("New numerical object is not an INT or FLOAT")
    logger.debug(f"✏️ NUMERIC CLASS SET AS {numeric_class}")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = insert(numerical_table)
        model_dict = new_numeric.model_dump(exclude_unset=True)
        del model_dict["numerical_type"]
        logger.debug(f"Model dict for inserting values: \n{model_dict}")
        stmt = stmt.values(**model_dict)
        logger.debug(f"Generated Statement: \n{stmt}")
        execute = session.execute(stmt)
        commit = session.commit()
        logger.debug(f"➕ Data_inserted")
    new_key = execute.inserted_primary_key[0]
    # return_numeric = new_numeric
    # return_numeric.pk_harm_num = execute.inserted_primary_key[0]
    with Session(engine) as session:
        logger.debug("Created second session")
        stmt = insert(harmonized_numeric_id_map)
        stmt = stmt.values(**{"fk_harm_num": new_key, "table_class": numeric_class})
        execute = session.execute(stmt)
        commit = session.commit()
    return get_numeric(numeric_id=new_key)


def update_numeric(numerical_update: Harm_numerical_union) -> Harm_numerical_union:
    logger.debug(f"{fa.service}{fa.update} {__name__} {stack()[0][3]}()")
    numeric_table, pydantic_class = get_numeric_table_by_uuid(
        numeric_id=numerical_update.pk_harm_num
    )
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = update(numeric_table)
        stmt = stmt.where(numeric_table.pk_harm_num == numerical_update.pk_harm_num)
        stmt = stmt.values()
        execute = session.execute(stmt)
        commit = session.commit()


def delete_numeric(numeric_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__} {stack()[0][3]}()")
    numeric_table, pydantic_class = get_numeric_table_by_uuid(numeric_id=numeric_id)
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = delete(numeric_table)
        stmt = stmt.where(numeric_table.pk_harm_num == numeric_id)
        execute = session.execute(stmt)
        commit = session.commit()
    return None
