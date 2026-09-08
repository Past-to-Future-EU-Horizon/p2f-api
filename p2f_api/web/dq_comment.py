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

router = APIRouter(prefix="/dq-comment", tags=["Data Quality Comment"])


@router.get("/{dataset_id}", operation_id="comment-list")
def list_dq_comments(auth: api_token_annotation,
                     dataset_id: uuid.UUID) -> List[DQ_Comment]:
    """List the comments for a specific dataset

    Args:
        auth (api_token_annotation): _description_
        dataset_id (uuid.UUID): Unique identifier of the dataset

    Returns:
        List[DQ_Comment]: List of the comments on the dataset
    """
    return dq_comment.list_dq_comments(dataset_id=dataset_id)


@router.post("/", operation_id="comment-create")
def create_dq_comment(auth: api_token_annotation,
                      new_comment: DQ_Comment) -> List[DQ_Comment]:
    """Create a new comment for a datasetc.

    Args:
        auth (api_token_annotation): _description_
        new_comment (DQ_Comment): New p2f-pydantic DQ_Comment object to associate with dataset

    Returns:
        List[DQ_Comment]: List of the comments on the dataset
    """
    # TODO check for email in new comment is authorized with provided token
    return dq_comment.create_dq_comment(new_comment=new_comment)


@router.put("/", operation_id="comment-update")
def update_dq_comment(auth: api_token_annotation,
                      update_comment: DQ_Comment) -> List[DQ_Comment]:
    """Update a comment on the dataset

    Args:
        auth (api_token_annotation): _description_
        update_comment (DQ_Comment): The updated comment in a p2f-pydantic DQ_Comment object. comment_id must be set.  

    Returns:
        List[DQ_Comment]: List of the comments on the dataset
    """
    # TODO check for email in updating comment is authorized with provided token
    return dq_comment.update_dq_comment(update_comment=update_comment)


@router.delete("/{comment_id}", operation_id="comment-delete")
def delete_dq_comment(auth: api_token_annotation,
                      comment_id: uuid.UUID):
    """Delete a comment from a dataset

    Args:
        auth (api_token_annotation): _description_
        comment_id (uuid.UUID): Unique identifier of the comment to be deleted  
    """
    return delete_dq_comment(comment_id=comment_id)
