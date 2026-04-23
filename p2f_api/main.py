# Local libraries
from p2f_api.apilogs import logger, fa
from p2f_api.web import datasets
from p2f_api.web import harm_data_record
from p2f_api.web import harm_numerical
from p2f_api.web import harm_data_metadata_location
from p2f_api.web import harm_data_type
from p2f_api.web import harm_timeslice
from p2f_api.web import harm_metadata_species
from p2f_api.web import harm_age
from p2f_api.web import harm_reference
from p2f_api.web import export_clean_ddl
from p2f_api.web import link_git
from p2f_api.web import doi
from p2f_api.web import dq_comment
from p2f_api.web import temp_accounts
from p2f_api.web import health
from p2f_api.service.temp_accounts import api_init
from p2f_pydantic import system as p2fsystem
# Third Party Libraries
from fastapi import FastAPI
# Batteries included libraries
import os

app = FastAPI(
    title="Past to Future Dataset API",
    summary="APIs for the P2F team to share datasets and conform to a harmonized data model",
    version="0.0.69",
)
logger.debug(f"{fa.background} {__name__}")
logger.debug("▶️  FastAPI() Started")

api_init()

# For Kubernetes heartbeat/healthchecks
app.include_router(health.router)

# Main data Types
app.include_router(datasets.router)
app.include_router(harm_numerical.router)
app.include_router(harm_data_record.router)
app.include_router(harm_data_metadata_location.router)
app.include_router(harm_data_type.router)
app.include_router(harm_timeslice.router)
app.include_router(harm_metadata_species.router)
app.include_router(harm_age.router)
app.include_router(harm_reference.router)
app.include_router(link_git.router)
app.include_router(doi.router)
# app.include_router(dq_comment.router)
app.include_router(temp_accounts.router)

@app.get("/version")
def get_api_metadata() -> p2fsystem.API_Metadata:
    minimum_p2f_client_py = p2fsystem.Semantic_Version(major=0, 
                                                       minor=0, 
                                                       patch=19)
    api_version = p2fsystem.Semantic_Version(major=0, 
                                             minor=0, 
                                             patch=69)
    return_class = p2fsystem.API_Metadata(pyclient_minimum_version=minimum_p2f_client_py, 
                                          api_system_version=api_version)
    return return_class

# Debugging features
P2F_DDL = bool(os.getenv("P2F_DDL", default=False))
if P2F_DDL:
    app.include_router(export_clean_ddl.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app)
