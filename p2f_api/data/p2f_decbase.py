# Local libraries
from p2f_api.apilogs import logger, fa
# Third Party Libraries
from sqlalchemy.orm import declarative_base
# Batteries included libraries

logger.debug(f"{fa.data} {__name__}")

baseSQL = declarative_base()