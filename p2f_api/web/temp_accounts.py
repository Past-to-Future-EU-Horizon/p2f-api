from p2f_api.apilogs import logger, fa
from ..service import temp_accounts
from p2f_pydantic.temp_accounts import Temp_Account, Authorization_Check
from p2f_pydantic.generic import Message

# Third Party Libraries
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi import BackgroundTasks
from fastapi import Security
from fastapi import Header
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from furl import furl

# Batteries included libraries
from typing import Literal, Optional, Annotated
from inspect import stack

router = APIRouter(prefix="/token", tags=["Basic Account"])

api_token = APIKeyHeader(name="x-p2f-token")

api_email = Header(alias="x-p2f-email")

@router.post("/request")
def request_token(request_token: Temp_Account,
                  background_task: BackgroundTasks) -> JSONResponse:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    background_task.add_task(temp_accounts.token_request, request_token.email)
    # temp_accounts.token_request(request_token.email)
    # We always return the same message.
    ## For security reasons do not reveal permitted email addresses.
    msg = "Your token request has been received, if your email is valid, you will receive a token through your email soon."
    # msg = Message(message=msg)
    return JSONResponse(content={"status": msg})

@router.post("/data-upload-check", 
             operation_id="data-upload-check",
             include_in_schema=False)
def data_upload_check(request: Request, 
                      auth: Temp_Account) -> Authorization_Check:
    """This method is intended to act as a check on the token and email address. 
        TODO: Add a check for the location of the incoming request. This check 
            needs to look if the request is coming from the portal. """
    result = combined_auth(request=request,
                           token=auth.token,
                           email=auth.email)
    return Authorization_Check(authorized=result)

def authentication(email: str, token: str) -> bool:
    logger.debug(f"{fa.web}{fa.auth} {__name__} {stack()[0][3]}()")
    token_match = temp_accounts.evaluate_token(email=email, token=token)
    if token_match == "NotFound":
        logger.debug("AUTHENTICATION RESULT: Token not found, raising 401 Unauthorized.")
        return False
        # raise HTTPException(status_code=401, detail="Unauthorized: Token not found")
    elif token_match == "Expired":
        logger.debug("AUTHENTICATION RESULT: Token expired, raising 401 Unauthorized.")
        return False
        # raise HTTPException(status_code=401, detail="Unauthorized: Token expired")
    elif token_match == "Authorized":
        logger.debug("AUTHENTICATION RESULT: Token success, returning True.")
        return True

def authorization(
    endpoint: str,
    operation: Literal["get", "post", "put", "delete"],
    email: Optional[str]=None,
) -> bool:
    logger.debug(f"{fa.web}{fa.auth} {__name__} {stack()[0][3]}()")
    result = temp_accounts.is_action_authorized(email=email, endpoint=endpoint, operation=operation)
    logger.debug(f"AUTHORIZATION RESULT: {result}")
    return result

def combined_auth(request: Request,
                  token: str = Security(api_token), 
                  email: str = api_email):
    logger.debug(f"{fa.web}{fa.auth} {__name__} {stack()[0][3]}()")
    operation = request.method.lower()
    logger.debug(f"Operation: {operation}")
    path_furl = furl(request.url)
    logger.debug(f"path_furl: {path_furl}")
    endpoint = path_furl.path.segments[0]
    logger.debug(f"endpoint: {endpoint}")
    # Generally we will allow GET operations, if an operation is allowed by public 
    #    return true
    if email is None:
        logger.debug("Auth is None path taken")
        return authorization(endpoint=endpoint, 
                             operation=operation)
    else:
        logger.debug("Authentication and authorization paths taken")
        a1 = authentication(email=email, token=token)
        a2 = authorization(endpoint=endpoint, 
                        email=email,
                        operation=operation)
        logger.debug(f"Authentication: {a1} -- Authorization: {a2}")
        if a1 == False:
            raise HTTPException(401, "Unauthenticated")
        if a2 == False:
            raise HTTPException(401, "Unauthorized")
        return a1 and a2
    
api_token_annotation = Annotated[api_token, Security(combined_auth)]