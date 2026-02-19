# Local libraries
from p2f_api.apilogs import logger, fa
from .harm_data_record import list_harm_data_record
from ..data.db_connection import engine
from ..data.harm_data_numerical import harmonized_float_confidence, harmonized_float
from ..data.harm_data_numerical import harmonized_int_confidence, harmonized_int
from ..data.harm_data_numerical import harmonized_numeric_id_map
from p2f_pydantic.harm_data_numerical import harmonized_float_confidence as Harmonized_float_confidence
from p2f_pydantic.harm_data_numerical import harmonized_int_confidence as Harmonized_int_confidence
from p2f_pydantic.harm_data_numerical import harmonized_float as Harmonized_float
from p2f_pydantic.harm_data_numerical import harmonized_int as Harmonized_int
from p2f_pydantic.harm_data_numerical import insert_harm_numerical as Insert_harm_numerical
from p2f_pydantic.harm_data_numerical import return_harm_numerical as Return_harm_numerical
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update

# Batteries included libraries
from typing import List, Union, Literal, Optional
from uuid import UUID
from inspect import stack

Harm_numerical_union = Union[
    Harmonized_float_confidence,
    Harmonized_float,
    Harmonized_int_confidence,
    Harmonized_int,
]

harm_table_matching = {
    "float_confidence": {
        "db": harmonized_float_confidence,
        "pydantic": Harmonized_float_confidence,
    },
    "float": {"db": harmonized_float, "pydantic": Harmonized_float},
    "int_confidence": {
        "db": harmonized_int_confidence,
        "pydantic": Harmonized_int_confidence,
    },
    "int": {"db": harmonized_int, "pydantic": Harmonized_int},
}


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


def list_numerics(
    record_hash: Optional[str] = None,
    numeric_type: Optional[
        Literal["float_confidence", "float", "int_confidence", "int"]
    ] = None,
    data_type: Optional[UUID] = None,
    dataset_id: Optional[UUID] = None,
) -> Return_harm_numerical:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    logger.debug(f"{locals()}")
    if dataset_id is not None:
        logger.debug("•  dataset_id is not none")
        # We are doing this out of the Session and lower iteration
        filtered_dataset_record_hashes = list_harm_data_record(dataset=dataset_id)
        filtered_dataset_record_hashes = tuple(
            {x.record_hash for x in filtered_dataset_record_hashes}
        )
        logger.debug(f"• {filtered_dataset_record_hashes}")
    with Session(engine) as session:
        session_results = harm_table_matching  # Copy the global table above
        logger.debug("•  Created session")
        table_match = list(
            harm_table_matching.keys()
        )  # Create a list to iterate through just below
        if numeric_type is not None:
            # overwrite the above list if numeric type
            table_match = [numeric_type]
        for table in table_match:  # iterated list
            logger.debug(f"•• Running table search for: {table}")
            stmt = select(harm_table_matching[table]["db"])
            if record_hash is not None:
                logger.debug("••• Condition added: record_hash")
                stmt = stmt.where(
                    harm_table_matching[table]["db"].fk_data_record == record_hash
                )
            if dataset_id is not None:
                logger.debug("••• Condition added: dataset_id")
                # reliant on the above dataset_id if statement
                stmt = stmt.where(
                    harm_table_matching[table]["db"].fk_data_record.in_(
                        filtered_dataset_record_hashes
                    )
                )
            if data_type is not None:
                logger.debug("••• Condition added: data_type")
                stmt = stmt.where(
                    harm_table_matching[table]["db"].fk_data_type == data_type
                )
            logger.debug(f"•• Generated statement: {stmt}")
            results = session.execute(stmt).all()
            logger.debug(f"•• Found {len(results)} results")
            session_results[table]["results"] = [
                session_results[table]["pydantic"](**x[0].__dict__) for x in results
            ]
    logger.debug("•  All results collected")
    return_results = Return_harm_numerical()
    for table in session_results.keys():
        match table:
            case "int":
                if len(session_results[table]["results"]) > 0:
                    return_results.data_harmonized_int = session_results[table][
                        "results"
                    ]
                    # return_results.data_harmonized_int = [x.model_dump(exclude_unset=True) for x in session_results[table]["results"]]
                else:
                    return_results.data_harmonized_int = None
            case "int_confidence":
                if len(session_results[table]["results"]) > 0:
                    return_results.data_harmonized_int_confidence = session_results[
                        table
                    ]["results"]
                    # return_results.data_harmonized_int_confidence = [x.model_dump(exclude_unset=True) for x in session_results[table]["results"]]
                else:
                    return_results.data_harmonized_int_confidence = None
            case "float":
                if len(session_results[table]["results"]) > 0:
                    return_results.data_harmonized_float = session_results[table][
                        "results"
                    ]
                    # return_results.data_harmonized_float = [x.model_dump(exclude_unset=True) for x in session_results[table]["results"]]
                else:
                    return_results.data_harmonized_float = None
            case "float_confidence":
                if len(session_results[table]["results"]) > 0:
                    return_results.data_harmonized_float_confidence = session_results[
                        table
                    ]["results"]
                    # return_results.data_harmonized_float_confidence = [x.model_dump(exclude_unset=True) for x in session_results[table]["results"]]
                else:
                    return_results.data_harmonized_float_confidence = None
    logger.debug("Results sorted and return object prepared")
    # logger.debug(f"##########\n{return_results}\n\n\n")
    return return_results


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


def create_numeric(new_numeric: Insert_harm_numerical) -> Insert_harm_numerical:
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
