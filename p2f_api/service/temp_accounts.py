# Local libraries
from p2f_api.apilogs import logger, fa
from .account_permissions_json import Account_Permissions
from .account_permissions_json import default_consortium_permissions
from .account_permissions_json import super_user
from .account_permissions_json import public_view
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
import traceback

dotenv.load_dotenv()

P2F_EMAIL_SA_USERNAME = os.getenv("P2F_EMAIL_SA_USERNAME")
P2F_EMAIL_SA_PASSWORD = os.getenv("P2F_EMAIL_SA_PASSWORD")
P2F_EMAIL_SA_PORT = int(os.getenv("P2F_EMAIL_SA_PORT", default=587))
P2F_EMAIL_SA_SERVER = os.getenv("P2F_EMAIL_SA_SERVER")
P2F_EMAIL_ADDRESS = os.getenv("P2F_EMAIL_ADDRESS")
P2F_EMAIL_IP_CIDR = ipaddress.ip_network(os.getenv("P2F_EMAIL_IP_CIDR"), strict=False)
P2F_EMAIL_IP_ACTIVE = bool(os.getenv("P2F_EMAIL_IP_ACTIVE", default=False))
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
        stmt = stmt.where(temp_tokens.expiration >= datetime.now(tz=ZoneInfo("UTC")))
        stmt = stmt.values(expiration=new_expiration_time)
        session.execute(stmt)
        session.commit()


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
    email_sending_status = False
    minimum_TLS_version = ssl.TLSVersion.TLSv1_2
    tc = 0
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    with smtplib.SMTP_SSL(host=P2F_EMAIL_SA_SERVER, 
                     port=P2F_EMAIL_SA_PORT,
                     context=ssl_context) as server:
        logger.debug("Server intiated")
        server.login(user=P2F_EMAIL_SA_USERNAME, password=P2F_EMAIL_SA_PASSWORD)
        logger.debug("Logged into server")
        server.sendmail(
                        from_addr=P2F_EMAIL_ADDRESS,
                        to_addrs=recipient,
                        msg=message.as_string()
                        )
        logger.debug("Sent email")
    
    # while email_sending_status == False and tc < 5:
    #     try:
    #         context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    #         context.minimum_version = minimum_TLS_version
    #         context.maximum_version = ssl.TLSVersion.TLSv1_3
    #         if minimum_TLS_version in [ssl.TLSVersion.TLSv1_3, ssl.TLSVersion.TLSv1_2, ssl.TLSVersion.TLSv1_1]:
    #             with smtplib.SMTP_SSL(
    #                 host=P2F_EMAIL_SA_SERVER,
    #                 port=P2F_EMAIL_SA_PORT,
    #                 context=context
    #             ) as server:
    #                 server.login(user=P2F_EMAIL_SA_USERNAME,
    #                             password=P2F_EMAIL_SA_PASSWORD)
    #                 server.sendmail(
    #                     from_addr=P2F_EMAIL_ADDRESS,
    #                     to_addrs=recipient,
    #                     msg=message.as_string()
    #                 )
    #         else:
    #             with smtplib.SMTP_SSL(
    #                 host=P2F_EMAIL_SA_SERVER,
    #                 port=P2F_EMAIL_SA_PORT
    #             ) as server:
    #                 server.login(user=P2F_EMAIL_SA_USERNAME,
    #                             password=P2F_EMAIL_SA_PASSWORD)
    #                 server.sendmail(
    #                     from_addr=P2F_EMAIL_ADDRESS,
    #                     to_addrs=recipient,
    #                     msg=message.as_string()
    #                 )
    #     except Exception as e:
    #         logger.debug(f"Error encountered in Email {e}")
    #         logger.debug(f"{traceback.format_exc()}")
    #         tc += 1
    #         if minimum_TLS_version in [ssl.TLSVersion.TLSv1_3, ssl.TLSVersion.TLSv1_2, ssl.TLSVersion.TLSv1_1]:
    #             if minimum_TLS_version == ssl.TLSVersion.TLSv1_3:
    #                 logger.debug("TLS version downgraded to TLSv1_2")
    #                 minimum_TLS_version = ssl.TLSVersion.TLSv1_2
    #             elif minimum_TLS_version == ssl.TLSVersion.TLSv1_2:
    #                 logger.debug("TLS version downgraded to TLSv1_1")
    #                 minimum_TLS_version = ssl.TLSVersion.TLSv1_1
    #             elif minimum_TLS_version == ssl.TLSVersion.TLSv1_1:
    #                 logger.debug("TLS version downgraded to no TLS")
    #                 minimum_TLS_version = None
    #     if tc >= 5:
    #         raise ConnectionAbortedError(f"Could not auth and connect with {P2F_EMAIL_SA_SERVER}")

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
    if P2F_EMAIL_IP_ACTIVE:
        send_email(message=message, recipient=email)
        email_history_update(email_uuid=email_uuid, receipient=email, status="Created")

def last_request(email: EmailStr):
    with Session(engine) as session:
        # We use the email history to do the check, as we do not want a situation where
        #   a user requests a token in quick succession, then checks just under 5 min
        #   later, and then have to wait another 5 minutes before the API will take action
        stmt = select(email_history.creation_timestamp)
        stmt = stmt.where(email_history.email_meta_receiver == email)
        stmt = stmt.order_by(email_history.creation_timestamp.desc())
        result = session.execute(stmt).first()
    if result is not None:
        logger.debug(f"•• Result found for email history, returning {result[0]}")
        # return the result no matter the time
        return result[0]
    else:
        # if no result then send something that will be valid for creating a new token
        logger.debug(f"•• No result found, returning {datetime.now(tz=ZoneInfo('UTC')) - timedelta(days=1)}")
        return datetime.now(tz=ZoneInfo("UTC")) - timedelta(days=1)

def token_request(email: EmailStr):
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    # Check if the email address is allowed
    if is_permitted_address(email=email): 
        # Check timing of last request
        lr = last_request(email=email)
        now = datetime.now(tz=ZoneInfo("UTC"))
        fivecalc = lr + timedelta(seconds=(5*60))
        NOWP5_EVAL = now <= fivecalc
        logger.debug(f"Now value and calculation lr {lr} -- now {now} -- fivecalc {fivecalc}")
        if NOWP5_EVAL:
            logger.debug(f"•• Email address {email} had a request within the past 5 minutes, doing nothing.")
        else:
            logger.debug(f"•• Email address {email} did not have a request within the past 5 minutes, generating new code.")
            invalidate_current_token(email=email)
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
    endpoint: str,
    operation: Literal["get", "insert", "update", "delete"],
    email: Optional[EmailStr]=None,
) -> bool:
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    if email is not None:
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
    else: 
        return public_view[endpoint][operation]


insert_permitted_address(email=P2F_ADMIN_EMAIL_ADDRESS,
                         permissions=super_user)
