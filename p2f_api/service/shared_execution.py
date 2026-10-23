from typing import Literal
from io import BytesIO, StringIO
from inspect import stack
import pandas as pd
from sqlalchemy.sql import Executable
from sqlalchemy.orm import Session
from fastapi import Response
from pydantic import BaseModel
from p2f_api.apilogs import logger, fa
from data.db_connection import engine

mimes = Literal["text/csv", "application/json", "application/vnd.apache.parquet"]




def strip_fk(column_name: str) -> str:
    logger.debug(f"{fa.service}{fa.other} {stack()[0][3]}()")
    if column_name[:3] == "fk_":
        column_name = column_name[3:]
    return column_name

def remove_table_metadata(input_df: pd.DataFrame) -> pd.DataFrame:
    logger.debug(f"{fa.service}{fa.other} {stack()[0][3]}()")
    columns = input_df.columns
    # remove foreign key indicators and remove creation and update datetime
    output_columns = [x for x in columns 
                      if x not in ["creation_timestamp",
                                   "update_timestamp"]]
    # remove primary key
    output_columns = [x for x in output_columns
                      if x[:3] != "pk_"]
    output_df = input_df[output_columns]
    return output_df

def get(
        stmt: Executable,
        pydantic_object: BaseModel,
        session_object: Session,
        output_format: mimes
        ): 
    logger.debug(f"{fa.service}{fa.get} {stack()[0][3]}()")
    logger.debug(f"SHARED EXECUTION GET STMT: {stmt}")
    logger.debug(f"SHARED EXECUTION OUTPUT FORMAT: {output_format}")
    match output_format:
        case "application/json":
            result = session_object.execute(stmt).first()
            logger.debug(f"SHARED EXECUTION GET RESULT: {result}")
            result = pydantic_object(**result[0].__dict__)
            return result
        case "application/vnd.apache.parquet":
            result = pd.read_sql(stmt, engine)
            result = remove_table_metadata(result)
            logger.debug(f"SHARED EXECUTION COLUMNS: {result.columns}")
            file_object = BytesIO()
            result = result.to_parquet(file_object)
            return Response(content=file_object.getvalue(),
                            media_type=output_format)
        case "text/csv":
            result = pd.read_sql(stmt, engine)
            result = remove_table_metadata(result)
            logger.debug(f"SHARED EXECUTION COLUMNS: {result.columns}")
            file_object = StringIO()
            result = result.to_parquet(file_object)
            return Response(content=file_object.getvalue(),
                            media_type=output_format)

def list(
        stmt: Executable,
        pydantic_object: BaseModel,
        session_object: Session,
        output_format: mimes
        ):
    logger.debug(f"{fa.service}{fa.list} {stack()[0][3]}()")
    logger.debug(f"SHARED EXECUTION LIST STMT: {stmt}")
    logger.debug(f"SHARED EXECUTION OUTPUT FORMAT: {output_format}")
    logger.debug(f"SHARED EXECUTION RECEIVED PYDANTIC OBJECT: {repr(pydantic_object)}")
    match output_format:
        case "application/json":
            results = session_object.execute(stmt).all()
            logger.debug(f"Found {len(results)} results")
            results = [pydantic_object(**x[0].__dict__) for x in results]
            # logger.debug(f"SHARED EXECUTION LIST application/json RESULT: {results}")
            return results
        case "application/vnd.apache.parquet":
            results = pd.read_sql(stmt, engine)
            results = remove_table_metadata(results)
            logger.debug(f"SHARED EXECUTION COLUMNS: {results.columns}")
            file_object = BytesIO()
            results = results.to_parquet(file_object)
            return Response(content=file_object.getvalue(),
                            media_type=output_format)
        case "text/csv":
            results = pd.read_sql(stmt, engine)
            results = remove_table_metadata(results)
            logger.debug(f"SHARED EXECUTION COLUMNS: {results.columns}")
            file_object = StringIO()
            results = results.to_csv(file_object)
            return Response(content=file_object.getvalue(),
                            media_type=output_format)


def create(
        stmt: Executable,
        session_object: Session,
        ) -> int: # Output is the inserted PK
    logger.debug(f"{fa.service}{fa.create} {stack()[0][3]}()")
    execute = session_object.execute(stmt)
    commit = session_object.commit()
    return execute.inserted_primary_key[0]

# def update(
#         stmt: Executable,
#         pydantic_object: BaseModel,
#         database_object: baseSQL,
#         session_object: Session,
#         output_format: mimes
#         ):
#     pass

def delete(
        stmt: Executable,
        session_object: Session,
        ):
    logger.debug(f"{fa.service}{fa.delete} {stack()[0][3]}()")
    execute = session_object.execute(stmt)
    commit = session_object.commit()
    return None