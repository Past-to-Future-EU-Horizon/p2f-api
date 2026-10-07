# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import harm_core
from p2f_pydantic.harm_core import Core, CoreSegment
from .temp_accounts import api_token_annotation

tag_name = "HARM Core"

router = APIRouter(prefix="/harm-core", tags=[tag_name])

tag_metadata = {"name": tag_name,
                "description": 
                """HARM Core is made of two components, the core and the core segment. """}

# List Cores
@router.get("/", operation_id="core-list")
def list_cores(auth: api_token_annotation,) -> List[Core]:
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    return harm_core.list_cores()

# List Core Segments
@router.get("/{core_id}/segment", operation_id="core-segment-list")
def list_core_segments(auth: api_token_annotation,
                       core_id: uuid.UUID) -> List[CoreSegment]:
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    return harm_core.list_core_segments(core_id=core_id)

# Get Core
@router.get("/{core_id}", operation_id="core-get")
def get_core(auth: api_token_annotation,
             core_id: uuid.UUID | None=None) -> Core:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_core.get_core(core_id=core_id)

# Get Segment
@router.get("/{core_id}/segment/{core_segment_id}", operation_id="core-segment-get")
def get_core_segment(auth: api_token_annotation,
                     core_id: uuid.UUID | None= None, 
                     core_segment_id: uuid.UUID | None=None) -> CoreSegment:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_core.get_core_segment(core_id=core_id, 
                                      core_segment_id=core_segment_id)

# Create Core
@router.post("/", operation_id="core-create")
def create_core(auth: api_token_annotation,
                new_core: Core) -> Core:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_core.create_core(new_core=new_core)

# Create Segment
@router.post("/{core_id}/segment", operation_id="core-segment-create")
def create_core_segment(auth: api_token_annotation,
                        core_id: uuid.UUID, 
                        new_core_segment: CoreSegment) -> CoreSegment:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_core.create_core_segment(new_core_segment=new_core_segment, 
                                         core_id=core_id)

# Delete Core
@router.delete("/{core_id}", operation_id="core-delete")
def delete_core(auth: api_token_annotation,
                core_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_core.delete_core(core_id=core_id)

# Delete Segment
@router.delete("/{core_id}/segment/{core_segment_id}", operation_id="core-segment-delete")
def delete_core_segment(auth: api_token_annotation,
                        core_id: uuid.UUID, 
                        core_segment_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_core.delete_core_segment(core_id=core_id, core_segment_id=core_segment_id)

@router.post("/segment/{core_segment_id}/assign/{record_hash}", operation_id="core-segment_record-assign")
def assign_core_segment_to_record(auth: api_token_annotation,
                                  core_segment_id: uuid.UUID,
                                  record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.assign} {__name__} {stack()[0][3]}()")
    return harm_core.assign_core_segment_to_record(core_segment_id=core_segment_id, 
                                                   record_hash=record_hash)

@router.delete("/segment/{core_segment_id}/remove/{record_hash}", operation_id="core-segment_record-remove")
def remove_core_segment_from_record(auth: api_token_annotation,
                                    core_segment_id: uuid.UUID,
                                    record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.remove} {__name__} {stack()[0][3]}()")
    return harm_core.remove_core_segment_from_record(core_segment_id=core_segment_id,
                                                     record_hash=record_hash)