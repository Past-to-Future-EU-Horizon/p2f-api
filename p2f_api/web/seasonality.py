# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import seasonality as season_svc
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.seasonality import Season, Seasonality_DS
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router_ds = APIRouter(prefix="/seasonality")
router_rec = APIRouter(prefix="/season")

# Get
@router_ds.get("/{dataset_id}")
def get_seasonality_ds(dataset_id: uuid.UUID) -> Seasonality_DS:
    return season_svc.get_seasonality_ds(dataset_id=dataset_id)

@router_rec.get("/{record_hash}")
def get_season_rec(record_hash: str) -> Season:
    return season_svc.get_season_rec(record_hash=record_hash)

# Create
@router_ds.post("/{dataset_id}")
def add_seasonality_ds(dataset_id: uuid.UUID,
                       seasonality: str) -> Seasonality_DS:
    return season_svc.add_seasonality_ds(dataset_id=dataset_id,
                                          seasonality=seasonality)
    
@router_rec.post("/{record_hash}")
def add_season_rec(record_hash: str, 
                   season: str) -> Season:
    return season_svc.add_season_rec(record_hash=record_hash,
                                     season=season)
# Delete
@router_ds.delete("/{dataset_id}")
def delete_seasonality_ds(dataset_id: uuid.UUID) -> None:
    return season_svc.delete_seasonality_ds(dataset_id=dataset_id)

@router_rec.delete("/{record_hash}")
def delete_season_rec(record_hash: str) -> None:
    return season_svc.delete_season_rec(record_hash==record_hash)