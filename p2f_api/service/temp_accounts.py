# Local libraries
from p2f_api.apilogs import logger
from ..data.db_connection import engine
from ..data.temp_accounts import temp_accounts, permitted_domains
from p2f_pydantic.temp_accounts import temp_accounts as Temp_account
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from pydantic import EmailStr
# Batteries included libraries
from typing import List, Optional
from datetime import datetime, timedelta
from secrets import token_urlsafe
from functools import wraps


def insert_token_record(email: str,
                  generated_token: str, 
                  expiration: datetime) -> str:
    logger.debug("➡️Inserting Token Record")
    with Session(engine) as session:
        stmt = insert(temp_accounts)
        stmt = stmt.values(
            email=email,
            token=generated_token, 
            expiration=expiration
        )
        execute = session.execute(stmt)
        commit = session.commit()

def send_email_information(email: EmailStr, 
                           generated_token: str, 
                           expiration: datetime):
    logger.debug("📩Sending token to email")
    

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

def get_token(
    email: Optional[str]=None,
    token: Optional[str]=None,
    ) -> Temp_account:
    with Session(engine) as session:
        stmt = select(temp_accounts)
        if email:
            stmt = stmt.where(temp_accounts.email==email)
        if token:
            stmt = stmt.where(temp_accounts.token==token)
        result = session.execute(stmt).first()
    return Temp_account(**result.tuple()[0].__dict__)

def list_permitted_domains() -> List[str]:
    with Session(engine) as session:
        stmt = select(permitted_domains.domain)
        results = session.execute(stmt)
    return results

def insert_permitted_domain(domain):
    with Session(engine) as session:
        stmt = insert(permitted_domains)
        stmt = stmt.values(domain)
        execute = session.execute(stmt)
        commit = session.commit()

