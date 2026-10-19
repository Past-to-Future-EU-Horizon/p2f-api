from typing import Literal
from io import BytesIO
import pandas as pd
from sqlalchemy.sql import Executable
from sqlalchemy.orm import Session
from pydantic import BaseModel

mimes = Literal["text/csv", "application/json", "application/vnd.apache.parquet"]

def strip_fk(column_name: str) -> str:
    if column_name[:3] == "fk_":
        column_name = column_name[3:]
    return column_name

def remove_table_metadata(input_df: pd.DataFrame) -> pd.DataFrame:
    columns = input_df.columns
    # remove foreign key indicators and remove creation and update datetime
    output_columns = [strip_fk(x) for x in columns 
                      if x not in ["creation_timestamp",
                                   "update_timestamp"]]
    # remove primary key
    output_columns = [x for x in columns
                      if x[:3] != "pk_"]
    output_df = input_df[output_columns]
    return output_df

def get(
        stmt: Executable,
        pydantic_object: BaseModel,
        session_object: Session,
        output_format: mimes
        ): 
    match output_format:
        case "application/json":
            result = session_object.execute(stmt).first()
            result = pydantic_object(**result.__dict__)
        case "application/vnd.apache.parquet":
            result = pd.read_sql(stmt, session_object)
            result = remove_table_metadata(result)
            file_object = BytesIO()
            result = result.to_parquet(file_object)
        case "text/csv":
            result = pd.read_sql(stmt, session_object)
            result = remove_table_metadata(result)
            file_object = BytesIO()
            result = result.to_parquet(file_object)
    return result

def list(
        stmt: Executable,
        pydantic_object: BaseModel,
        session_object: Session,
        output_format: mimes
        ):
    match output_format:
        case "application/json":
            results = session_object.execute(stmt).all()
            results = [pydantic_object(**x.__dict__) for x in results]
        case "application/vnd.apache.parquet":
            results = pd.read_sql(stmt, session_object)
            results = remove_table_metadata(results)
            file_object = BytesIO()
            results = results.to_parquet(file_object)
        case "text/csv":
            results = pd.read_sql(stmt, session_object)
            results = remove_table_metadata(results)
            file_object = BytesIO()
            results = results.to_csv(file_object)
    return results


def create(
        stmt: Executable,
        session_object: Session,
        ) -> int: # Output is the inserted PK
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
    execute = session_object.execute(stmt)
    commit = session_object.commit()
    return None