# Local libraries
from p2f_api.apilogs import logger, fa
# from .create_metadata import create_metadata
from .p2f_decbase import baseSQL
from .datasets import *
from .harm_data_metadata import *
from .harm_data_numerical import *
from .harm_data_record import *
from .harm_data_types import *
from .harm_age import *
from .harm_reference import *
from .harm_text import *
from .harm_timeslice import *

# Third Party Libraries
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from dotenv import load_dotenv
# Batteries included libraries
import os
import pathlib

logger.debug(f"{fa.data} {__name__}")

p = pathlib.Path(os.getcwd())
print(p)

logger.debug("LOADING dotenv")
de = load_dotenv()
print(de)
logger.debug("dotenv LOADED")

PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
PG_HOST = os.getenv("PG_HOST")
PG_DB = os.getenv("PG_DB")
PG_PORT = int(os.getenv("PG_PORT", 5432))

connection_str = f"postgresql+psycopg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
logger.debug("Database connection url:" + connection_str.replace(PG_PASS, "♦" * len(PG_PASS)))

engine = create_engine(connection_str)
baseSQL.metadata.create_all(engine)
# logger.debug(dir(baseSQL.metadata))
# logger.debug(baseSQL.metadata.naming_convention)
# logger.debug(baseSQL.metadata.info)
# logger.debug(baseSQL.metadata.tables)
# for table in baseSQL.metadata.tables.items():
#     logger.debug(CreateTable(table[1]))