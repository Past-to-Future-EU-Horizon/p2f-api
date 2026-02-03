from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
# Batteries included libraries

# record hash sizes ----------------------------------------
## sha1      40
## sha256    64
## sha384    96
## sha512   128
## md5       32
#### TODO Make this into a real dictionary and config option

logger.debug(f"{fa.data} {__name__}")

class harm_data_record(baseSQL):
    __tablename__ = "p2f_harm_data_record"
    pk_harm_data_record: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_dataset: Mapped[str] = mapped_column(ForeignKey("p2f_datasets.dataset_identifier"))
    record_hash: Mapped[str] = mapped_column(String(32), index=True, unique=True)