# Batteries included libraries
import uuid
from typing import List, Optional
from inspect import stack

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update

from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.seasonality import season, seasonality_ds
from service import shared_execution
from p2f_pydantic.seasonality import Season, Seasonality_DS

# Get 
def get_seasonality_ds(dataset_id: uuid.UUID,
                       output_format: shared_execution.mimes = "application/json",) -> Seasonality_DS:
    logger.debug(f"{fa.service}{fa.get} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(seasonality_ds)
        stmt = stmt.where(seasonality_ds.dataset_id == dataset_id)
        result = shared_execution.get(stmt=stmt, 
                                      pydantic_object=Seasonality_DS,
                                      session_object=session,
                                      output_format="application/json")
    return result

def get_season_rec(record_hash: str,
                   output_format: shared_execution.mimes = "application/json",) -> Season:
    logger.debug(f"{fa.service}{fa.get} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(season)
        stmt = stmt.where(season.record_hash == record_hash)
        result = shared_execution.get(stmt=stmt, 
                                      pydantic_object=Season,
                                      session_object=session,
                                      output_format="application/json")
    return result

# Create
def add_seasonality_ds(new_seasonality: Seasonality_DS,
                       output_format: shared_execution.mimes = "application/json",) -> Seasonality_DS:
    logger.debug(f"{fa.service}{fa.create} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(seasonality_ds)
        stmt = stmt.values(
            dataset_id = new_seasonality.dataset_id,
            seasonality = new_seasonality.seasonality_type
        )
        # logger.debug(f"Seasonality create statement: {stmt}")
        shared_execution.create(stmt=stmt,
                                session_object=session)
    return get_seasonality_ds(dataset_id=new_seasonality.dataset_id,
                              output_format=output_format)

def add_season_rec(new_season: Season,
                   output_format: shared_execution.mimes = "application/json",) -> Season:
    logger.debug(f"{fa.service}{fa.create} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(season)
        stmt = stmt.values(
            record_hash = new_season.record_hash,
            season = new_season.season
        )
        # logger.debug(f"Seasonality create statement: {stmt}")
        pk = shared_execution.create(stmt=stmt,
                                     session_object=session)
    return get_season_rec(record_hash=new_season.record_hash,
                          output_format=output_format)

# Delete
def delete_seasonality_ds(dataset_id: uuid.UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(seasonality_ds)
        stmt = stmt.where(seasonality_ds.dataset_id == dataset_id)
        shared_execution.delete(stmt=stmt,
                                session_object=session)

def delete_season_rec(record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.delete} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(season)
        stmt = stmt.where(season.record_hash == record_hash)
        shared_execution.delete(stmt=stmt,
                                session_object=session)