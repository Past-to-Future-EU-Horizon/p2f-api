# Local libraries
from p2f_api.apilogs import logger
from .account_permissions_json import Account_Permissions
from ..data.db_connection import engine
from ..data.temp_accounts import temp_tokens, permitted_addresses, email_history
from p2f_pydantic.temp_accounts import temp_accounts as Temp_account
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from pydantic import EmailStr
# Batteries included libraries
from typing import List, Optional, Literal
from datetime import datetime, timedelta
from secrets import token_urlsafe
from functools import wraps
from zoneinfo import ZoneInfo

def insert_token_record(email: EmailStr,
                  generated_token: str, 
                  expiration: datetime) -> str:
    logger.debug("➡️Inserting Token Record")
    with Session(engine) as session:
        stmt = insert(temp_tokens)
        stmt = stmt.values(
            email=email,
            token=generated_token, 
            expiration=expiration
        )
        execute = session.execute(stmt)
        commit = session.commit()

def invalidate_current_token(
        email: EmailStr
    ):
    pass

def send_email_information(email: EmailStr, 
                           generated_token: str, 
                           expiration: datetime):
    logger.debug("📩Sending token to email")
    with Session(engine) as session:
        pass
    

def token_request(email: EmailStr):
    new_token = str(token_urlsafe(256))[:127]
    expiration = datetime.now() + timedelta(hours=2)
    logger.debug('🪙Generated token')
    insert_token_record(email=email, 
                        generated_token=new_token,
                        expiration=expiration)
    logger.debug('🪙➡️📩Token inserted, emailing token')
    send_email_information(email=email, 
                           generated_token=new_token,
                           expiration=expiration)
    logger.debug('🌐📩Email sent')

def evaluate_token(
    email: EmailStr, 
    token: str
    ) -> Literal["Authorized", "Expired", "NotFound"]:
    with Session(engine) as session:
        stmt = select(temp_tokens)
        stmt = stmt.where(temp_tokens.email==email)
        stmt = stmt.where(temp_tokens.token==token)
        result = session.execute(stmt).first()
    if result is None:
        return "NotFound"
    else:
        if result[0].expiration < datetime.now():
            return "Expired"

def insert_permitted_address(email: EmailStr,
                             permissions: Account_Permissions):
    pass 
