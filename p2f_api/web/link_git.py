# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import link_git
from p2f_pydantic.link_git import Git_Repository
# Third Party Libraries
from fastapi import Body, APIRouter, Request
# Batteries included libraries
import uuid
from typing import Optional, List
from inspect import stack

router = APIRouter(prefix="/git")

# List
@router.get("/")
def list_git_repositories(dataset_id: Optional[uuid.UUID]=None) -> List[Git_Repository]:
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    return link_git.list_git(dataset_id=dataset_id)

# Get Single
@router.get("/{git_repo_id}")
def get_git_repo(git_repo_id: Optional[uuid.UUID]=None) -> Git_Repository:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return link_git.get_git(git_repo_id=git_repo_id)

# Create
@router.post("/")
def create_git_repo(new_git_repo: Git_Repository,
                    dataset_id: Optional[uuid.UUID]=None) -> Git_Repository:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return link_git.create_git_repo(new_git_repo, dataset_id)

# Delete
@router.delete("/{git_repo_id}")
def delete_git_repo(git_repo_id: Optional[uuid.UUID]=None) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return link_git.delete_git_repo(git_repo_id)

# Assign
@router.post("/assign")
def assign_git_repo(git_repo_id: uuid.UUID,
                    dataset_id: uuid.UUID):
    logger.debug(f"{fa.web}{fa.assign} {__name__} {stack()[0][3]}()")
    return link_git.assign_git_repo(git_repo_id, dataset_id)

# Remove
@router.delete("/remove")
def unlink_git_repo(git_repo_id: uuid.UUID,
                    dataset_id: uuid.UUID):
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return link_git.unlink_git_repo(git_repo_id, dataset_id)