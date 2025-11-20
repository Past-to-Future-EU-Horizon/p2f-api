# Local libraries
from p2f_api.apilogs import logger
from data.db_connection import engine
from data.db_connection import baseSQL
from sqlalchemy.schema import CreateTable

def get_clean_ddl():
    sql = ""
    for table in baseSQL.metadata.sorted_tables:
        # logger.debug(repr(table))
        sql += str(CreateTable(table).compile(engine))
        sql += ";\n"
    return sql