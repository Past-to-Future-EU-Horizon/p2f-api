from p2f_api.apilogs import logger, fa
from ..service import dq_comment
from p2f_pydantic.data_quality import dq_comment as DQ_Comment
# Third Party Libraries
from fastapi import Body, APIRouter, Request
# Batteries included libraries
import uuid
from typing import Optional, List
from inspect import stack

router = APIRouter(prefix="/dq-comment")

@router.get("/{dataset_id}")
def list_dq_comments(dataset_id: uuid.UUID) -> List[DQ_Comment]:
    return dq_comment.list_dq_comments(dataset_id=dataset_id)

@router.post("/")
def create_dq_comment(new_comment: DQ_Comment) -> List[DQ_Comment]:
    # TODO check for email in new comment is authorized with provided token
    return dq_comment.create_dq_comment(new_comment=new_comment)

@router.update("/")
def update_dq_comment(update_comment: DQ_Comment) -> List[DQ_Comment]:
    # TODO check for email in updating comment is authorized with provided token
    return dq_comment.update_dq_comment(update_comment=update_comment)

@router.delete("/{comment_id}")
def delete_dq_comment(comment_id: uuid.UUID):
    return delete_dq_comment(comment_id=comment_id)