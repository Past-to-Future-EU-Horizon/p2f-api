# Local libraries
from p2f_api.apilogs import logger, fa
from .account_permissions_json import Account_Permissions
from .account_permissions_json import default_consortium_permissions
from .account_permissions_json import super_user
from ..data.db_connection import engine
from ..data.temp_accounts import temp_tokens, permitted_addresses, email_history

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from pydantic import EmailStr
import dotenv

# Batteries included libraries
from typing import List, Optional, Literal, Union
from datetime import datetime, timedelta
from secrets import token_urlsafe
from zoneinfo import ZoneInfo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import ipaddress
from subprocess import run
import json
from uuid import uuid4, UUID
import hashlib
import os
from inspect import stack

dotenv.load_dotenv()

P2F_EMAIL_SA_USERNAME = os.getenv("P2F_EMAIL_SA_USERNAME")
P2F_EMAIL_SA_PASSWORD = os.getenv("P2F_EMAIL_SA_PASSWORD")
P2F_EMAIL_SA_PORT = int(os.getenv("P2F_EMAIL_SA_PORT", default=587))
P2F_EMAIL_SA_SERVER = os.getenv("P2F_EMAIL_SA_SERVER")
P2F_EMAIL_ADDRESS = os.getenv("P2F_EMAIL_ADDRESS")
P2F_EMAIL_IP_CIDR = ipaddress.ip_network(os.getenv("P2F_EMAIL_IP_CIDR"), strict=False)
P2F_ADMIN_EMAIL_ADDRESS = os.getenv("P2F_ADMIN_EMAIL_ADDRESS")
P2F_SALT = os.getenv("P2F_SALT", default=token_urlsafe(256))
P2F_TOKEN_TTL = int(os.getenv("P2F_TOKEN_TTL", default=(24 * 3600)))
P2F_HASH_COUNT = int(os.getenv("P2F_HASH_COUNT", default=2000))
P2F_TOKEN_DEBUG = bool(os.getenv("P2F_TOKEN_DEBUG", default=False))
P2F_TOKEN_LENGTH = int(os.getenv("P2F_TOKEN_LENGTH", default=64))


def hashorama(password: str) -> str:
    logger.debug(f"{fa.background}{fa.service} {__name__} {stack()[0][3]}()")
    c = 0
    h_input = password
    while c <= P2F_HASH_COUNT:
        # if c % 100 == 0:
        # logger.debug(f"•• Hash run {c}")
        h = hashlib.sha512()
        h.update(h_input.encode("utf8"))
        h.update(P2F_SALT.encode("utf8"))
        h_input = str(h.hexdigest())
        c += 1
    return h_input

def insert_token_record(email: str,
                  generated_token: str, 
                  expiration: datetime):
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    logger.debug("➡️Inserting Token Record")
    hashed_token = hashorama(generated_token)
    with Session(engine) as session:
        stmt = insert(temp_tokens)
        stmt = stmt.values(
            email_address=email, token=hashed_token, expiration=expiration
        )
        execute = session.execute(stmt)
        commit = session.commit()
    logger.debug("Token inserted into database")


def invalidate_current_token(email: EmailStr):
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    new_expiration_time = datetime.now(tz=ZoneInfo("UTC")) - timedelta(seconds=1)
    with Session(engine) as session:
        stmt = update(temp_tokens)
        stmt = stmt.where(temp_tokens.email_address == email)
        stmt = stmt.where(temp_tokens.expiration <= datetime.now(tz=ZoneInfo("UTC")))
        stmt = stmt.values(expiration=new_expiration_time)


def create_email_message(email: EmailStr, generated_token: str, expiration: datetime):
    message = MIMEMultipart("alternative")
    message["Subject"] = "P2F Portal Token"
    message["From"] = P2F_EMAIL_ADDRESS
    message["To"] = email
    basic_text = f"""
Your token for the P2F Portal is below:
{generated_token}

This token will expire on {expiration}. 

This is an automated email from the P2F API, for questions email {P2F_ADMIN_EMAIL_ADDRESS}.
Do not reply to this email directly. """
    message.attach(MIMEText(basic_text, "plain"))
    if P2F_TOKEN_DEBUG:
        logger.debug(message)
    return message


def email_history_update(email_uuid: UUID, receipient: str, status: str = "Created"):
    with Session(engine) as session:
        stmt = select(email_history)
        stmt = stmt.where(email_history.email_id == email_uuid)
        existing = session.execute(stmt).all()
        if len(existing) > 0:
            stmt = update(email_history)
            stmt = stmt.where(email_history.email_id == email_uuid)
            stmt = stmt.values(status=status)
        else:
            stmt = insert(email_history)
            stmt = stmt.values(
                email_id=email_uuid,
                status=status,
                sending_time=datetime.now(tz=ZoneInfo("UTC")),
                email_meta_sender=P2F_EMAIL_ADDRESS,
                email_meta_receiver=receipient,
                email_meta_subject="P2F Portal Token",
            )
        execute = session.execute(stmt)
        commit = session.commit()


def send_email(message: MIMEMultipart,
               recipient: str):
    logger.debug(f"{fa.background}{fa.service} {__name__} {stack()[0][3]}()")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        host=P2F_EMAIL_SA_SERVER,
        port=P2F_EMAIL_SA_PORT,
        context=context
    ) as server:
        server.login(user=P2F_EMAIL_SA_USERNAME,
                     password=P2F_EMAIL_SA_PASSWORD)
        server.sendmail(
            from_addr=P2F_EMAIL_ADDRESS,
            to_addrs=recipient,
            msg=message.as_string()
        )


def check_host_ip() -> bool:
    """Check the IP address of the host so we don't accidentally try to send an email from outside our requested IP range.

    :return: bool
    :rtype: bool
    """
    logger.debug(f"{fa.background}{fa.service} {__name__} {stack()[0][3]}()")
    status = False
    try:
        IPADDRS = []
        ipaddrs = run(["ip", "-4", "-brief", "-json", "a"], capture_output=True)
        ipaddrs = json.loads(ipaddrs.stdout.decode("utf8"))
        for ip_rec in ipaddrs:
            if ip_rec["ifname"] not in ["lo"]:
                if len(ip_rec["addr_info"]) == 1:
                    IPADDRS.append(ip_rec["addr_info"][0]["local"])
                    if (
                        ipaddress.ip_address(ip_rec["addr_info"][0]["local"])
                        in P2F_EMAIL_IP_CIDR
                    ):
                        status = True
                if len(ip_rec["addr_info"]) > 1:
                    # prefixed = {prefix: addr for prefix, addr in } This could probably be comprehensioned
                    prefixed = {}
                    for addr_rec in ip_rec["addr_info"]:
                        prefixed[addr_rec["prefixlen"]] = addr_rec["local"]
                    IPADDRS.append(prefixed[min(list(prefixed.keys()))])
                    if (
                        ipaddress.ip_address(prefixed[min(list(prefixed.keys()))])
                        in P2F_EMAIL_IP_CIDR
                    ):
                        status = True
    except Exception as e:
        logger.debug(f"{stack()[0][3]}() experienced an error: {e}")
    if P2F_TOKEN_DEBUG:
        logger.debug(f"{stack()[0][3]}() evaluated {IPADDRS}")
        logger.debug(f"{stack()[0][3]}() returning {status}")
    return status


def send_email_information(email: EmailStr, generated_token: str, expiration: datetime):
    logger.debug(f"{fa.background}{fa.service} {__name__} {stack()[0][3]}()")
    logger.debug("📩Sending token to email")

    email_uuid = uuid4()
    message = create_email_message(
        email=email,
        generated_token=generated_token,
        expiration=expiration
    )
    email_history_update(email_uuid=email_uuid, receipient=email, status="Created")
    if check_host_ip():
        send_email(message=message, recipient=email)


def token_request(email: EmailStr):
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    if is_permitted_address(email=email):
        new_token = str(token_urlsafe(256))[:P2F_TOKEN_LENGTH]
        expiration = datetime.now(tz=ZoneInfo("UTC")) + timedelta(seconds=P2F_TOKEN_TTL)
        logger.debug("🪙Generated token")
        if P2F_TOKEN_DEBUG:
            # Don't run this in production, leaky tokens sink shifts.
            logger.debug(
                f"Newly generated token for {email}\n{new_token}\nExpiring on {expiration.isoformat()}"
            )
        insert_token_record(
            email=email,
            generated_token=new_token,
            expiration=expiration
        )
        logger.debug("🪙➡️📩Token inserted, emailing token")
        send_email_information(
            email=email,
            generated_token=new_token,
            expiration=expiration
        )
        logger.debug("🌐📩Email sent")


def evaluate_token(
    email: EmailStr, 
    token: str
) -> Literal["Authorized", "Expired", "NotFound"]:
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    token = hashorama(token)
    with Session(engine) as session:
        stmt = select(temp_tokens)
        stmt = stmt.where(temp_tokens.email_address == email)
        stmt = stmt.where(temp_tokens.token == token)
        result = session.execute(stmt).first()
    if result is None:
        return "NotFound"
    else:
        if result[0].expiration < datetime.now(tz=ZoneInfo("UTC")):
            return "Expired"
        else:
            return "Authorized"


def insert_permitted_address(
    email: EmailStr,
    permissions: Account_Permissions = default_consortium_permissions,
    timezone: str = "Europe/Amsterdam",
):
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        del_stmt = delete(permitted_addresses).where(permitted_addresses == email)
        execute_del_stmt = session.execute(del_stmt)
        stmt = insert(permitted_addresses)
        stmt = stmt.values(
            email_address=email,
            permissions=permissions.model_dump_json(exclude_unset=True),
            timezone=timezone,
        )
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


def is_action_authorized(
    email: EmailStr,
    endpoint: str,
    operation: Literal["get", "insert", "update", "delete"],
) -> bool:
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    with Session(engine) as session:
        stmt = select(permitted_addresses.permissions)
        stmt = stmt.where(permitted_addresses.email_address == email)
        result = session.execute(stmt).first()
    if result:
        # logger.debug(result)
        permission_json = json.loads(result[0])
        # logger.debug(permission_json)
        # permissions = Account_Permissions(permission_json).model_dump(exclude_unset=True)
        return permission_json[endpoint][operation]
    else:
        return False


insert_permitted_address(email=P2F_ADMIN_EMAIL_ADDRESS,
                         permissions=super_user)
