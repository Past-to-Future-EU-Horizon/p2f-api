# Local libraries
from .apilogs import logger
# Third Party Libraries
from fastapi import FastAPI
# Batteries included libraries

app = FastAPI()
logger.debug("▶️  FastAPI() Started")

if __name__ == "__main__":
    import uvicorn
    app.run()