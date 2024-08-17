from fastapi import FastAPI
import logging
from app.core.config import settings
from app.core.logging import configure_logging

# Configure logging with the level specified in settings
logging_level = getattr(logging, settings.logging_level.upper(), logging.INFO)
configure_logging(level=logging_level)

app = FastAPI()


@app.get("/")
async def read_root():
    """
    Root endpoint to check the status of the API.
    """
    if settings.debug:
        logging.debug("API root endpoint accessed in debug mode.")
    else:
        logging.info(f"API root endpoint accessed in {settings.environment} mode.")
    return {"message": "Welcome to the FastAPI application!"}
