# Local libraries
from p2f_api.apilogs import logger
from p2f_api.web import datasets, harm_data_record, harm_numerical
from p2f_api.web import harm_data_metadata_location, harm_data_type
from p2f_api.web import harm_timeslice
# Third Party Libraries
from fastapi import FastAPI
# Batteries included libraries

app = FastAPI(
    title="Past to Future Dataset API",
    summary="APIs for the P2F team to share datasets and conform to a harmonized data model",
    version="0.0.1"
)
logger.debug("▶️  FastAPI() Started")

app.include_router(datasets.router)
app.include_router(harm_numerical.router)
app.include_router(harm_data_record.router)
app.include_router(harm_data_metadata_location.router)
app.include_router(harm_data_type.router)
app.include_router(harm_timeslice.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app)