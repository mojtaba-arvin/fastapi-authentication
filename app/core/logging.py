import logging
import sys
from app.core.config import settings


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configures the logging settings for the application.

    Args:
        level: The logging level to set (e.g., logging.DEBUG, logging.INFO).
    """
    # Check if the root logger already has handlers
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=level,
            handlers=[
                logging.StreamHandler(sys.stdout),
                # Additional handlers can be added here if needed
            ]
        )
        logger = logging.getLogger(__name__)
        logger.info("Logging has been configured.")


# Initialize logging with the level specified in settings
logging_level = getattr(logging, settings.logging_level.upper(), logging.INFO)
configure_logging(level=logging_level)
