from p2f_api.apilogs import logger, fa
from ..service import temp_accounts
from p2f_pydantic.temp_accounts import Temp_Account
from p2f_pydantic.generic import Message

# Third Party Libraries
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from furl import furl

# Batteries included libraries
from typing import Literal, Optional
from inspect import stack

router = APIRouter(prefix="/token")


@router.post("/foo")
def request_token(request_token: Temp_Account) -> JSONResponse:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    temp_accounts.token_request(request_token.email)
    # We always return the same message.
    ## For security reasons do not reveal permitted email addresses.
    msg = "Your token request has been received, if your email is valid, you will receive a token through your email soon."
    # msg = Message(message=msg)
    return JSONResponse(content={"status": msg})


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
    operation: Literal["get", "insert", "update", "delete"],
    email: Optional[str]=None,
) -> bool:
    logger.debug(f"{fa.web}{fa.auth} {__name__} {stack()[0][3]}()")
    return temp_accounts.is_action_authorized(email, endpoint, operation)

def combined_auth(request: Request,
                  auth: Optional[Temp_Account]=None):
    logger.debug(f"{fa.web}{fa.auth} {__name__} {stack()[0][3]}()")
    operation = request.method.lower()
    path_furl = furl(request.url)
    endpoint = path_furl.path.segments[0]
    # Generally we will allow GET operations, if an operation is allowed by public 
    #    return true
    if auth is None:
        return authorization(endpoint=endpoint, 
                             operation=operation)
    else:
        a1 = authentication(auth=auth)
        a2 = authorization(endpoint=endpoint, 
                        email=auth.email,
                        operation=operation)
        logger.debug(f"Authentication: {a1} -- Authorization: {a2}")
        return a1 and a2