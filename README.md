# p2f-api
API Layer for the Past to Future projects Portal. Past to Future is an EU Horizon funded project. 

*v0.0.19*

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
* P2F_EMAIL_SA_PORT = 587
* P2F_EMAIL_SA_SERVER
* P2F_EMAIL_ADDRESS
* P2F_EMAIL_IP_CIDR
* P2F_ADMIN_EMAIL_ADDRESS
* P2F_TOKEN_TTL = 24*3600 (1 day)
* P2F_SALT = `secrets.token_urlsafe(256)`
* P2F_HASH_COUNT = 2000
* P2F_TOKEN_DEBUG = False
* P2F_TOKEN_LENGTH = 64

Debug management 

* P2F_DDL

## Installation

Clone this repoository locally, cd into the p2f_api subfolder, and run uvicorn main:app

OR

Run the container found on ghcr.io for this API. 

In any case you need a PostgreSQL database (other databases are not supported), API tested with v17 and v18. 