from data.db_connection import baseSQL
from sqlalchemy.schema import CreateTable

def get_clean_ddl():
    sql = ""
    for table in baseSQL.metadata.tables.items():
        sql += str(CreateTable(table[1]))
        sql += ";\n"
    return sql