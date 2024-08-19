import logging
from fastapi import FastAPI
from ariadne.asgi import GraphQL
from app.core.config import settings
from app.core.logging import configure_logging
from app.api.graphql.schema.mutations import schema


# Configure logging with the level specified in settings
logging_level = getattr(logging, settings.logging_level.upper(), logging.INFO)
configure_logging(level=logging_level)

app = FastAPI()


# GraphQL endpoint
app.add_route("/graphql", GraphQL(schema))


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
