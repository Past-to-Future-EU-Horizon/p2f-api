# p2f-api
API Layer for the Past to Future projects Portal. Past to Future is an EU Horizon funded project. 


## Environment Variables

Defaults after the `=` sign. 

The API relies on PostgreSQL for a database, at this moment no other database platform is supported.

* PG_USER
* PG_PASS
* PG_HOST
* PG_PORT = 5432
* PG_DB

Account management

* P2F_EMAIL_SA_USERNAME
* P2F_EMAIL_SA_PASSWORD
* P2F_EMAIL_ADDRESS
* P2F_ADMIN_EMAIL_ADDRESS
* P2F_TOKEN_TTL = 24*3600 (1 day)
* P2F_SALT = `secrets.token_urlsafe(256)`
* P2F_HASH_COUNT = 2000
* P2F_TOKEN_DEBUG = False
* P2F_TOKEN_LENGTH = 64