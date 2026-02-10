# Local libraries
from p2f_api.apilogs import logger, fa
from .account_permissions_json import Account_Permissions, default_consortium_permissions
from ..data.db_connection import engine
from ..data.temp_accounts import temp_tokens, permitted_addresses, email_history
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from pydantic import EmailStr
# Batteries included libraries
from typing import List, Optional, Literal, Union
from datetime import datetime, timedelta
from secrets import token_urlsafe
from functools import wraps
from zoneinfo import ZoneInfo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from uuid import uuid4
import os
from inspect import stack

P2F_EMAIL_SA_USERNAME = os.getenv("P2F_EMAIL_SA_USERNAME")
P2F_EMAIL_SA_PASSWORD = os.getenv("P2F_EMAIL_SA_PASSWORD")
P2F_EMAIL_ADDRESS = os.getenv("P2F_EMAIL_ADDRESS")
P2F_TOKEN_TTL = os.getenv("P2F_TOKEN_TTL", default=(24*3600))

def insert_token_record(email: EmailStr,
                  generated_token: str, 
                  expiration: datetime) -> str:
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
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
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    new_expiration_time = datetime.now(tz=ZoneInfo("UTC")) - timedelta(seconds=1)
    with Session(engine) as session:
        stmt = update(temp_tokens)
        stmt = stmt.where(temp_tokens.email_address==email)
        stmt = stmt.where(temp_tokens.expiration<=datetime.now(tz=ZoneInfo("UTC")))
        stmt = stmt.values(expiration=new_expiration_time)

def send_email_information(email: EmailStr, 
                           generated_token: str, 
                           expiration: datetime):
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    logger.debug("📩Sending token to email")

    email_uuid = uuid4()

    message = MIMEMultipart("alternative")
    message["Subject"] = "P2F Portal Token"
    message["From"] = P2F_EMAIL_ADDRESS
    message["To"] = email
    basic_text = f"""\
Your one day token for the P2F Portal is below:
{generated_token}

This token will expire on {expiration}. 

This is an automated email from the P2F API, for questions email g.t.speed@uu.nl.
Do not reply to this email directly. """
    message.attach(MIMEText(basic_text, "plain"))
    with Session(engine) as session:
        stmt = insert(email_history)
        stmt = stmt.values(
            email_id=email_uuid,
            status="Created", 
            sending_time=datetime.now(tz=ZoneInfo("UTC")), 
            email_meta_sender=P2F_EMAIL_ADDRESS,
            email_meta_receiver=email,
            email_meta_subject="P2F Portal Token"
        )
        execute = session.execute(stmt)
        commit = session.commit()

def token_request(email: EmailStr):
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    if is_permitted_address(email=email):
        new_token = str(token_urlsafe(256))[:127]
        expiration = datetime.now(tz=ZoneInfo("UTC")) + timedelta(hours=2)
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
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(temp_tokens)
        stmt = stmt.where(temp_tokens.email_address==email)
        stmt = stmt.where(temp_tokens.token==token)
        result = session.execute(stmt).first()
    if result is None:
        return "NotFound"
    else:
        if result[0].expiration < datetime.now(tz=ZoneInfo("UTC")):
            return "Expired"
        else: 
            return "Authorized"

def insert_permitted_address(email: EmailStr,
                             permissions: Account_Permissions=default_consortium_permissions, 
                             timezone: str="Europe/Amsterdam"):
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = insert(permitted_addresses)
        stmt = stmt.values(email_address=email, 
                           permissions=permissions,
                           timezone=timezone)
        execute = session.execute(stmt)
        commit = session.commit()

def is_permitted_address(email: EmailStr) -> bool:
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(permitted_addresses)
        stmt = stmt.where(permitted_addresses.email_address == email)
        result = session.execute(stmt).first()
    if result:
        return True
    else: 
        return False

def is_action_authorized(email: EmailStr, 
                         endpoint: str, 
                         operation: Literal["get", "insert", "update", "delete"]) -> bool:
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(permitted_addresses)
        stmt = stmt.where(permitted_addresses.email_address == email)
        result = session.execute(stmt).first()
    if result:
        permissions = Account_Permissions(**result[0]).model_dump(exclude_unset=True)
        return permissions[endpoint][operation]
    else: 
        return False