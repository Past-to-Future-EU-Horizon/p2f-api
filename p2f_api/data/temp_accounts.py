# Local libraries
from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Double
from sqlalchemy import Text, String
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
# Batteries included libraries
from datetime import datetime

logger.debug(f"{fa.data} {__name__}")

class temp_accounts(baseSQL):
    __tablename__ = "TEMP_accounts_NOV2025CONGRESS"
    pk_temp_accounts: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(127), nullable=False)
    token: Mapped[str] = mapped_column(String(127), nullable=False)
    expiration: Mapped[datetime] = mapped_column(DateTime, nullable=False)

class permitted_domains(baseSQL):
    __tablename__ = "TEMP_accounts_domains"
    pk_temp_domains: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    domain: Mapped[str] = mapped_column(String(100))