# Local libraries
from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.link_git import git_repository, git_repository_to_dataset
from p2f_pydantic.link_git import Git_Repository
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
import uuid
from typing import List, Optional
from inspect import stack

def list_git_repositories(dataset_id: Optional[uuid.UUID]=None) -> List[Git_Repository]:
    logger.debug(f"{fa.service}{fa.list} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(git_repository)
        if dataset_id is not None:
            stmt_2 = select(git_repository_to_dataset)
            stmt_2 = stmt_2.where(git_repository_to_dataset.fk_dataset == dataset_id)
        results = session.execute(stmt).all()
    return [Git_Repository(x) for x in results]

def get_git_repo(git_repo_id: Optional[uuid.UUID]=None,
                 pk_git_repo: Optional[int]=None) -> Git_Repository:
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(git_repository)
        if git_repo_id is not None:
            stmt.where(git_repository.git_repo_id == git_repo_id)
        if pk_git_repo is not None:
            stmt.where(git_repository.pk_git_repo == pk_git_repo)
        result = session.execute(stmt).first()
    return Git_Repository(**result[0])

def create_git_repo(new_git_repo: Git_Repository,
                    dataset_id: Optional[uuid.UUID]=None) -> Git_Repository:
    logger.debug(f"{fa.service}{fa.create} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(git_repository)
        stmt = stmt.values(git_repo_url=new_git_repo.git_repo_id,
                           is_p2f_repo=new_git_repo.is_p2f_repo)
        execute = session.execute(stmt)
        commit = session.commit()
    return get_git_repo(pk_git_repo=execute.inserted_primary_key[0])

def delete_git_repo(git_repo_id: Optional[uuid.UUID]=None) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__}")
    with Session(engine) as session:
        stmt = delete(git_repository)
        stmt = stmt.where(git_repository.git_repo_id == git_repo_id)
        execute = session.execute(stmt)
        commit = session.commit()

def assign_git_repo(git_repo_id: uuid.UUID,
                    dataset_id: uuid.UUID):
    logger.debug(f"{fa.service}{fa.assign} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(git_repository_to_dataset)
        stmt = stmt.values(fk_git_repository=git_repo_id,
                           fk_dataset_id=dataset_id)
        execute = session.execute(stmt)
        commit = session.commit()

def unlink_git_repo(git_repo_id: uuid.UUID,
                    dataset_id: uuid.UUID):
    logger.debug(f"{fa.service}{fa.remove} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = delete(git_repository_to_dataset)
        stmt = stmt.where(git_repository_to_dataset.fk_dataset_id == dataset_id)
        stmt = stmt.where(git_repository_to_dataset.fk_git_repository == git_repo_id)
        execute = session.execute(stmt)
        commit = session.commit()