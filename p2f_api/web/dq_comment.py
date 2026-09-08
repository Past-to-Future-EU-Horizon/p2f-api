from p2f_api.apilogs import logger, fa
from ..service import dq_comment
from .temp_accounts import combined_auth, api_token_annotation, api_token_annotation
from p2f_pydantic.data_quality import DQ_Comment

# Third Party Libraries
from fastapi import Body, APIRouter, Request

# Batteries included libraries
import uuid
from typing import Optional, List
from inspect import stack

tag_name = "Data Quality Comment"

router = APIRouter(prefix="/dq-comment", tags=[tag_name])

tag_metadata = {"name": tag_name,
                "description": """Data quality comments are comments that are made on a dataset by a researcher within the 
                project to give an opinion or note on the inherent quality of a dataset. """}

@router.get("/{dataset_id}", operation_id="comment-list")
def list_dq_comments(auth: api_token_annotation,
                     dataset_id: uuid.UUID) -> List[DQ_Comment]:
    return dq_comment.list_dq_comments(dataset_id=dataset_id)


@router.post("/", operation_id="comment-create")
def create_dq_comment(auth: api_token_annotation,
                      new_comment: DQ_Comment) -> List[DQ_Comment]:
    # TODO check for email in new comment is authorized with provided token
    return dq_comment.create_dq_comment(new_comment=new_comment)


@router.put("/", operation_id="comment-update")
def update_dq_comment(auth: api_token_annotation,
                      update_comment: DQ_Comment) -> List[DQ_Comment]:
    # TODO check for email in updating comment is authorized with provided token
    return dq_comment.update_dq_comment(update_comment=update_comment)


@router.delete("/{comment_id}", operation_id="comment-delete")
def delete_dq_comment(auth: api_token_annotation,
                      comment_id: uuid.UUID):
    return delete_dq_comment(comment_id=comment_id)
