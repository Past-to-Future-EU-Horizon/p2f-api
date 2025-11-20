# Local libraries
from p2f_api.apilogs import logger
# Third Party Libraries
from fastapi import Body, APIRouter, Request
# Batteries included libraries
import uuid
from typing import Optional

router = APIRouter(prefix="/")

#List 
@router.get("/")
def list_() ->:
    pass

#Get Single
@router.get("/")
def get_() ->:
    pass

#Create
@router.post("/")
def create_() ->:
    pass

#Update 
@router.put("/")
def update_() ->:
    pass

@router.delete("/")
def delete_() ->:
    pass