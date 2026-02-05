# Local libraries
from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Uuid
from sqlalchemy import Text, String
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
# Batteries included libraries
from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

logger.debug(f"{fa.data} {__name__}")

class temp_tokens(baseSQL):
    __tablename__ = "p2f_account_tokens"
    pk_temp_accounts: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email_address: Mapped[str] = mapped_column(String(127), nullable=False)
    token: Mapped[str] = mapped_column(String(127), nullable=False)
    expiration: Mapped[datetime] = mapped_column(DateTime, nullable=False)

class permitted_addresses(baseSQL):
    __tablename__ = "p2f_accounts"
    pk_accounts: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email_address: Mapped[str] = mapped_column(String(127), nullable=False)
    permissions: Mapped[str] = mapped_column(Text, nullable=False)
    timezone: Mapped[str] = mapped_column(String, nullable=True, default="Europe/Amsterdam")

class  email_history(baseSQL):
    __tablename__ = "p2f_account_email_history"
    pk_email_history: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String(10), default="Created", nullable=False) # Created, Sent, Failure
    sending_time: Mapped[datetime] = mapped_column(DateTime(ZoneInfo("UTC")),)
    email_meta_sender: Mapped[str] = mapped_column(Text, nullable=False)
    email_meta_receiver: Mapped[str] = mapped_column(Text, nullable=False)
    email_meta_subject: Mapped[str] = mapped_column(Text, nullable=False)
    creation_timestamp: Mapped[datetime] = mapped_column(DateTime(ZoneInfo("UTC")),)
    update_timestamp: Mapped[datetime] = mapped_column(DateTime(ZoneInfo("UTC")),)
