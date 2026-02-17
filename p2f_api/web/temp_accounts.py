from p2f_api.apilogs import logger, fa
from ..service import temp_accounts
from p2f_pydantic.temp_accounts import Temp_Account
from p2f_pydantic.generic import Message
# Third Party Libraries
from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import EmailStr
# Batteries included libraries
from typing import Literal
from inspect import stack

router = APIRouter(prefix="/token")

@router.post("/request")
def request_token(request_token: Temp_Account) -> Message:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    temp_accounts.token_request(request_token.email)
    # We always return the same message. 
    ## For security reasons do not reveal permitted email addresses. 
    msg = "Your token request has been received, if your email is valid, you will receive a token through your email soon."
    msg = Message(message=msg)
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