# Batteries included libraries
# Third Party Libraries
from sqlalchemy.orm import declarative_base

# Local libraries
from p2f_api.apilogs import logger, fa

logger.debug(f"{fa.data} {__name__}")

baseSQL = declarative_base()
