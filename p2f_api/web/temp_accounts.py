from p2f_api.apilogs import logger, fa
from ..service import temp_accounts
from p2f_pydantic.temp_accounts import Temp_Account
from p2f_pydantic.generic import Message

# Third Party Libraries
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from furl import furl

# Batteries included libraries
from typing import Literal, Annotated, Union
from inspect import stack

router = APIRouter(prefix="/token")


@router.post("/request")
def request_token(request_token: Temp_Account) -> Message:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    temp_accounts.token_request(request_token.email)
    # We always return the same message.
    ## For security reasons do not reveal permitted email addresses.
    msg = "Your token request has been received, if your email is valid, you will receive a token through your email soon."
    msg = Message(message=msg)
    return msg


def authentication(auth: Temp_Account) -> bool:
    logger.debug(f"{fa.web}{fa.auth} {__name__} {stack()[0][3]}()")
    token_match = temp_accounts.evaluate_token(email=auth.email, token=auth.token)
    if token_match == "NotFound":
        raise HTTPException(status_code=401, detail="Unauthorized: Token not found")
    elif token_match == "Expired":
        raise HTTPException(status_code=401, detail="Unauthorized: Token expired")
    elif token_match == "Authorized":
        return True


def authorization(
    endpoint: str,
    email: str,
    operation: Literal["get", "insert", "update", "delete"],
) -> bool:
    logger.debug(f"{fa.web}{fa.auth} {__name__} {stack()[0][3]}()")
    return temp_accounts.is_action_authorized(email, endpoint, operation)

def combined_auth(auth: Temp_Account,
                  request: Request ):
    logger.debug(f"{fa.web}{fa.auth} {__name__} {stack()[0][3]}()")
    operation = request.method.lower()
    path_furl = furl(request.url)
    endpoint = path_furl.path.segments[0]
    a1 = authentication(auth=auth)
    a2 = authorization(endpoint=endpoint, 
                       email=auth.email,
                       operation=operation)
    logger.debug(f"Authentication: {a1} -- Authorization: {a2}")
    return a1 and a2