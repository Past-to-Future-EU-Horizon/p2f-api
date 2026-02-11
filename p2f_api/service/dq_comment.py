# Local libraries
from p2f_api.apilogs import logger, fa
from p2f_pydantic.data_quality import dq_comment as DQ_Comment
from ..data.db_connection import engine
from ..data.data_quality import dq_comment
from ..service.datasets import get_dataset
# Third Party Libraries
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
# Batteries included libraries
from uuid import UUID
from typing import List
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from inspect import stack

def list_dq_comments(dataset_id: UUID) -> List[DQ_Comment]:
    with Session(engine) as session:
        stmt = select(dq_comment)
        stmt = stmt.where(dq_comment.dataset_id == dataset_id)
        results = session.execute(stmt).all()
    return [dq_comment(**x.__dict__) for x in results]

def create_dq_comment(new_comment: DQ_Comment) -> List[DQ_Comment]:
    with Session(engine) as session:
        stmt = insert(dq_comment)
        stmt = stmt.values(**new_comment.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return list_dq_comments(dataset_id=new_comment.dataset_id)

def update_dq_comment(update_comment: DQ_Comment) -> List[DQ_Comment]:
    with Session(engine) as session:
        stmt = update(dq_comment)
        stmt = stmt.where(dq_comment.comment_id == update_comment.comment_id)
        stmt = stmt.values(**update_comment.model_dump(exclude_unset=True).pop("comment_id"))
        execute = session.execute(stmt)
        commit = session.commit()

def delete_dq_comment(comment_id: UUID):
    with Session(engine) as session:
        stmt = delete(dq_comment)
        stmt = stmt.where(dq_comment.comment_id == comment_id)
