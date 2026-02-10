from p2f_api.apilogs import logger, fa
from ..service import temp_accounts
from p2f_pydantic.harm_data_types import harm_data_type as Harm_data_type
# Third Party Libraries
from fastapi import Body, APIRouter, Request
from fastapi import HTTPException
from pydantic import EmailStr
# Batteries included libraries
import uuid
from typing import Literal, overload
from datetime import datetime
from inspect import stack

router = APIRouter(prefix="/token")

router.post("/request")
def request_token(email: EmailStr) -> str:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    temp_accounts.token_request(email)
    # We always return the same message. 
    ## For security reasons do not reveal permitted email addresses. 
    msg = "Your token request has been received, if your email is valid, you will receive a token through your email soon."
    return msg

def authentication(email: EmailStr, 
                  token: str):
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    token_match = temp_accounts.evaluate_token(email=email, 
                                          token=token)
    if token_match == "NotFound":
        raise HTTPException(status_code=401, detail="Unauthorized: Token not found")
    elif token_match == "Expired":
        raise HTTPException(status_code=401, detail="Unauthorized: Token expired")
    elif token_match == "Authorized":
        return True

def authorization(email: EmailStr, 
                  endpoint: str,
                  operation: Literal["get", "insert", "update", "delete"]):
    return temp_accounts.is_action_authorized(email, endpoint, operation)