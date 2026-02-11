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
# Third Party Libraries
from fastapi import FastAPI
# Batteries included libraries

app = FastAPI(
    title="Past to Future Dataset API",
    summary="APIs for the P2F team to share datasets and conform to a harmonized data model",
    version="0.0.1"
)
logger.debug(f"{fa.background} {__name__}")
logger.debug("▶️  FastAPI() Started")

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
app.include_router(dq_comment.router)

## Remember to remove in the future
app.include_router(export_clean_ddl.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app)