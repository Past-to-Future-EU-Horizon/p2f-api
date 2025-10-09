# Local libraries
from ..apilogs import logger
# from .create_metadata import create_metadata
from .p2f_decbase import baseSQL
from .datasets import *
from .harm_data_metadata import *
from .harm_data_numerical import *
from .harm_data_record import *
from .harm_data_types import *
# Third Party Libraries
from sqlalchemy import create_engine
from dotenv import load_dotenv
# Batteries included libraries
import os
import pathlib

p = pathlib.Path(os.getcwd())
print(p)

logger.debug("LOADING dotenv")
de = load_dotenv(override=True)
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