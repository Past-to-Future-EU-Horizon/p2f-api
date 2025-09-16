# Local libraries
from ..apilogs import logger
from data.db_connection import engine
from data.harm_data_numerical import harmonized_float_confidence, harmonized_float
from data.harm_data_numerical import harmonized_int_confidence, harmonized_int
from p2f_pydantic.harm_numerical import harmonized_float_confidence as Harmonized_float_confidence
from p2f_pydantic.harm_numerical import harmonized_int_confidence as Harmonized_int_confidence
from p2f_pydantic.harm_numerical import harmonized_float as Harmonized_float
from p2f_pydantic.harm_numerical import harmonized_int as Harmonized_int
from p2f_pydantic.harm_numerical import insert_harm_numerical as Insert_harm_numerical
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Union, Literal, Optional

Harm_numerical_union = Union[Harmonized_float_confidence, 
                             Harmonized_float,
                             Harmonized_int_confidence,
                             Harmonized_int]

harm_table_matching = {
    "float_confidence": {"db": harmonized_float_confidence, "pydantic": Harmonized_float_confidence}, 
    "float": {"db": harmonized_float, "pydantic": Harmonized_float}, 
    "int_confidence": {"db": harmonized_int_confidence, "pydantic": Harmonized_int_confidence}, 
    "int":  {"db": harmonized_int, "pydantic": Harmonized_int}, 
}

def list_numerics(record_hash: Optional[str]=None,
                  data_type: Optional[int]=None) -> List[Harm_numerical_union]:
    logger.debug("📃 service/harm_numerical.py list_numerics()")
    results_collection = []
    with Session(engine) as session:
        logger.debug("\tCreated session")
        for table in harm_table_matching.keys():
            logger.debug(f"\t\tRunning table search for: {table}")
            stmt = select(harm_table_matching[table]["db"])
            results = session.execute(stmt).all()
            logger.debug(f"\tFound {len(results)} results")
            results_collection += [harm_table_matching[table]["pydantic"](**x.tuple()) for x in results]
    return results_collection

def get_numeric(numeric_type: Optional[Literal["float_confidence", 
                                               "float", 
                                               "int_confidence", 
                                               "int"]]=None, 
                data_type: Optional[int]=None) -> Harm_numerical_union:
    logger.debug("🔎 service/harm_numerical.py get_numeric()")
    if numeric_type:
        numerical_table = harm_table_matching[numeric_type]["db"]
        with Session(engine) as session:
            logger.debug("\tCreated session")
            stmt = select(numerical_table)
            results = session.execute(stmt)
    else:
        results_collection = []
        with Session(engine) as session:
            logger.debug("\tCreated session")
            for table in harm_table_matching.keys():
                logger.debug(f"\t\tRunning table search for: {table}")
                stmt = select(harm_table_matching[table]["db"])
                results = session.execute(stmt).all()
                logger.debug(f"\tFound {len(results)} results")
                results_collection += [harm_table_matching[table]["pydantic"](**x.tuple()) for x in results]
        return results_collection


def create_numeric(new_dataset: Insert_harm_numerical) -> Harm_numerical_union:
    logger.debug("🆕 service/harm_numerical.py create_numeric()")
    if new_dataset.numerical_type == "INT":
        if new_dataset.upper_conf_value and new_dataset.lower_conf_value:
            numerical_table = harmonized_int_confidence
        else: 
            numerical_table = harmonized_int
    elif new_dataset.numerical_type == "FLOAT":
        if new_dataset.upper_conf_value and new_dataset.lower_conf_value:
            numerical_table = harmonized_float_confidence
        else:
            numerical_table = harmonized_float
    else: 
        raise ValueError("New numerical object is not an INT or FLOAT")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = insert(numerical_table)
        stmt = stmt.values()
        execute = session.execute(stmt)
        commit = session.commit()
    return_dataset = new_dataset
    return_dataset.pk_harm_data_record = execute.inserted_primary_key
    return return_dataset

def update_numeric(dataset_update: Harm_numerical_union) -> Harm_numerical_union:
    logger.debug("✏️ service/harm_numerical.py update_numeric()")
    #  numerical_table just below needs an explanation of what is happening. 
    ## We take the incoming update object and need to figure out which db table it goes in. 
    ## To do this, we can iterate through our pydantic objects and figure out which
    ##  pydantic object the incoming object matches. 
    ## Instead of writing several lines of iterator, I use a list comprehension to get
    ##  the db table value from the above dictionary, then use a conditional statement
    ##  in the comprehension to only take the matching isinstance table. 
    numerical_table = [harm_table_matching[x]["db"] for x in harm_table_matching.keys() if isinstance(dataset_update, harm_table_matching[x]["pydantic"])][0]
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = update(numerical_table)
        stmt = stmt.where(numerical_table.pk_harm_num == dataset_update.pk_harm_data_record)
        stmt = stmt.values()
        execute = session.execute(stmt)
        commit = session.commit()

def delete_numeric(existing_pk: int, 
                   numeric_type: Literal["float_confidence", "float", "int_confidence", "int"]) -> None:
    logger.debug("🗑️ service/harm_numerical.py delete_numeric()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        numerical_table = harm_table_matching[numeric_type]["db"]
        stmt = delete(numerical_table).where(numerical_table.pk_harm_num == existing_pk)
        execute = session.execute(stmt)
        commit = session.commit()
    return None
