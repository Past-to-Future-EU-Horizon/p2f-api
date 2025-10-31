# Local libraries
from ..apilogs import logger
from ..data.db_connection import engine
from ..data.harm_data_numerical import harmonized_float_confidence, harmonized_float
from ..data.harm_data_numerical import harmonized_int_confidence, harmonized_int
from ..data.harm_data_numerical import harmonized_numeric_id_map
from p2f_pydantic.harm_data_numerical import harmonized_float_confidence as Harmonized_float_confidence
from p2f_pydantic.harm_data_numerical import harmonized_int_confidence as Harmonized_int_confidence
from p2f_pydantic.harm_data_numerical import harmonized_float as Harmonized_float
from p2f_pydantic.harm_data_numerical import harmonized_int as Harmonized_int
from p2f_pydantic.harm_data_numerical import insert_harm_numerical as Insert_harm_numerical
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Union, Literal, Optional
from uuid import UUID

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

def get_numeric_table_by_uuid(numeric_id: UUID):
    logger.debug("🔎 service/harm_numerical.py get_numeric_table_by_uuid()")
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(harmonized_numeric_id_map)
        stmt = stmt.where(harmonized_numeric_id_map.fk_harm_num == numeric_id)
        result = session.execute(stmt).first()
    # logger.debug(dir())
    numeric_class = result.tuple()[0].table_class
    logger.debug(f"Numeric Class set as {numeric_class}")
    if numeric_class == "INT_CONFIDENCE":
        numeric_table = harmonized_int_confidence
        pydantic_class = Harmonized_int_confidence
    elif numeric_class == "INT":
        numeric_table = harmonized_int
        pydantic_class = Harmonized_int
    elif numeric_class == "FLOAT_CONFIDENCE":
        numeric_table = harmonized_float_confidence
        pydantic_class = Harmonized_float_confidence
    elif numeric_class == "FLOAT":
        numeric_table = harmonized_float
        pydantic_class = Harmonized_float
    return (numeric_table, pydantic_class)

def list_numerics(record_hash: Optional[str]=None,
                  numeric_type: Optional[Literal["float_confidence", 
                                               "float", 
                                               "int_confidence", 
                                               "int"]]=None, 
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

def get_numeric(numeric_id: UUID) -> Harm_numerical_union:
    logger.debug("🔎 service/harm_numerical.py get_numeric()")
    numeric_table, pydantic_class = get_numeric_table_by_uuid(numeric_id=numeric_id)
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = select(numeric_table)
        stmt = stmt.where(numeric_table.pk_harm_num == numeric_id)
        result = session.execute(stmt).first()
    numeric_object = pydantic_class(**result.tuple()[0].__dict__)
    return numeric_object


def create_numeric(new_numeric: Insert_harm_numerical) -> Insert_harm_numerical:
    logger.debug("🆕 service/harm_numerical.py create_numeric()")
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
        stmt = stmt.values(**model_dict)
        execute = session.execute(stmt)
        commit = session.commit()
        logger.debug(f"➕ Data_inserted")
    new_key = execute.inserted_primary_key[0]
    # return_numeric = new_numeric
    # return_numeric.pk_harm_num = execute.inserted_primary_key[0]
    with Session(engine) as session:
        stmt = insert(harmonized_numeric_id_map)
        stmt = stmt.values(**{"fk_harm_num": new_key, "table_class": numeric_class})
        execute = session.execute(stmt)
        commit = session.commit()
    return get_numeric(numeric_id=new_key)

def update_numeric(numerical_update: Harm_numerical_union) -> Harm_numerical_union:
    logger.debug("✏️ service/harm_numerical.py update_numeric()")
    numeric_table, pydantic_class = get_numeric_table_by_uuid(numeric_id=numerical_update.pk_harm_num)
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = update(numeric_table)
        stmt = stmt.where(numeric_table.pk_harm_num == numerical_update.pk_harm_num)
        stmt = stmt.values()
        execute = session.execute(stmt)
        commit = session.commit()

def delete_numeric(numeric_id: UUID) -> None:
    logger.debug("🗑️ service/harm_numerical.py delete_numeric()")
    numeric_table, pydantic_class = get_numeric_table_by_uuid(numeric_id=numeric_id)
    with Session(engine) as session:
        logger.debug("\tCreated session")
        stmt = delete(numeric_table)
        stmt = stmt.where(numeric_table.pk_harm_num == numeric_id)
        execute = session.execute(stmt)
        commit = session.commit()
    return None
