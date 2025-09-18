# Local libraries
from .apilogs import logger
from .web import datasets, harm_data_record, harm_numerical
# Third Party Libraries
from fastapi import FastAPI
# Batteries included libraries

app = FastAPI()
logger.debug("▶️  FastAPI() Started")

app.include_router(datasets.router)
app.include_router(harm_numerical.router)
app.include_router(harm_data_record.router)

if __name__ == "__main__":
    import uvicorn
    app.run()