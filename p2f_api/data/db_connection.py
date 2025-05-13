# Local libraries
from ..apilogs import logger
# Third Party Libraries
from sqlalchemy import create_engine
# Batteries included libraries
import os

PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
PG_HOST = os.getenv("PG_HOST")
PG_DB = os.getenv("PG_DB")
PG_PORT = int(os.getenv("PG_PORT", 5432))

connection_str = f"postgresql+psycopg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
logger.debug("Database connection url:" + connection_str.replace(PG_PASS, "♦" * len(PG_PASS)))

engine = create_engine(connection_str)