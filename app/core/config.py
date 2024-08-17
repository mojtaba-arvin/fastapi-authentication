from typing import Type, Dict, TypeVar
import os
import logging

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_core import ValidationError

# Define a type variable for configuration classes
ConfigType = TypeVar('ConfigType', bound='BaseConfig')


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BaseConfig(BaseSettings):
    project_name: str = Field(..., env="PROJECT_NAME")
    aws_region: str = Field(..., env="AWS_REGION")
    aws_cognito_user_pool_id: str = Field(..., env="AWS_COGNITO_USER_POOL_ID")
    aws_cognito_client_id: str = Field(..., env="AWS_COGNITO_CLIENT_ID")
    dynamodb_table_name: str = Field(..., env="DYNAMODB_TABLE_NAME")
    dynamodb_endpoint: str = Field(..., env="DYNAMODB_ENDPOINT")
    s3_bucket_name: str = Field(..., env="S3_BUCKET_NAME")
    logging_level: str = Field('INFO', env="LOGGING_LEVEL")
    environment: str = Field('DEVELOPMENT', env="ENVIRONMENT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @classmethod
    def get_configuration(cls) -> ConfigType:
        """
        Factory method to select and return the appropriate configuration class
        based on the ENVIRONMENT variable.
        """
        environment = os.getenv('ENVIRONMENT', 'DEVELOPMENT').upper()
        config_classes: Dict[str, Type[ConfigType]] = {
            'PRODUCTION': ProductionConfig,
            'STAGING': StagingConfig,
            'DEVELOPMENT': DevelopmentConfig
        }
        config_class = config_classes.get(environment, DevelopmentConfig)
        return config_class()


class DevelopmentConfig(BaseConfig):
    debug: bool = True


class StagingConfig(BaseConfig):
    debug: bool = False


class ProductionConfig(BaseConfig):
    debug: bool = False


def load_settings() -> BaseConfig:
    """
    Load the settings and handle any validation errors.
    """
    try:
        config_instance = BaseConfig.get_configuration()
        # No need to call config_instance.validate() in Pydantic v2.x
        return config_instance
    except ValidationError as e:
        logger.error("Configuration validation error:")
        for error in e.errors():
            field_location = " -> ".join(map(str, error['loc']))
            error_message = error['msg']
            logger.error(f"Field: {field_location}, Error: {error_message}")
        raise


# Instantiate the settings object based on the current environment
settings = load_settings()

# Configure logging level based on settings
if settings.logging_level.upper() == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

logger.info(f"Running in {settings.environment} environment with logging level {settings.logging_level}")
