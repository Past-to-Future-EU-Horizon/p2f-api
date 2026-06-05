from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.seasonality import season, seasonality_ds
from p2f_pydantic.seasonality import Season, Seasonality_DS

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update

# Batteries included libraries
import uuid
from typing import List, Optional
from inspect import stack

# Get 
def get_seasonality_ds(dataset_id: uuid.UUID) -> Seasonality_DS:
    logger.debug(f"{fa.service}{fa.get} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(seasonality_ds)
        stmt = stmt.where(seasonality_ds.dataset_id == dataset_id)
        result = session.execute(stmt).first()
    return Seasonality_DS(result)

def get_season_rec(record_hash: str) -> Season:
    logger.debug(f"{fa.service}{fa.get} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(season)
        stmt = stmt.where(season.record_hash == record_hash)
        result = session.execute(stmt).first()
    return Season(result)

# Create
def add_seasonality_ds(dataset_id: uuid.UUID,
                       seasonality: str) -> Seasonality_DS:
    logger.debug(f"{fa.service}{fa.create} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(seasonality_ds)
        stmt = stmt.values(
            dataset_id = dataset_id,
            seasonality = seasonality
        )
        execute = session.execute(stmt)
        commit = session.commit()
    return get_seasonality_ds(dataset_id=dataset_id)

def add_season_rec(record_hash: str, 
                   season: str) -> Season:
    logger.debug(f"{fa.service}{fa.create} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(season)
        stmt = stmt.values(
            record_hash = record_hash,
            season = season
        )
        execute = session.execute(stmt)
        commit = session.commit()
    return get_season_rec(record_hash=record_hash)

# Delete
def delete_seasonality_ds(dataset_id: uuid.UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(seasonality_ds)
        stmt = stmt.where(seasonality_ds.dataset_id == dataset_id)
        session.execute(stmt)
        session.commit()

def delete_season_rec(record_hash: str) -> None:
    logger.debug(f"{fa.service}{fa.delete} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(season)
        stmt = stmt.where(season.record_hash == record_hash)
        session.execute(stmt)
        session.commit()