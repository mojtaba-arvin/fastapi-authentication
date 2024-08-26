from fastapi import Depends, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.exceptions import UnauthorizedException
from app.core.dependency_injector import DependencyInjector, ServiceScope
from app.services.aws.cognito.auth import CognitoServiceInterface, CognitoService


http_bearer = HTTPBearer()

injector = DependencyInjector()
injector.register(CognitoServiceInterface, CognitoService, scope=ServiceScope.SCOPED)


async def get_access_token(credentials: HTTPAuthorizationCredentials = Security(http_bearer)):
    if not credentials:
        # TODO custom exception for access token
        raise UnauthorizedException()

    access_token = credentials.credentials

    if not validate_access_token(access_token):
        # TODO custom exception for access token
        raise UnauthorizedException()

    return access_token


async def get_refresh_token(request: Request) -> str:
    """
    Extracts the refresh token from the request headers.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        str: The refresh token.

    Raises:
        HTTPException: If the Refresh-Token header is missing or invalid.
    """
    refresh_header = request.headers.get("Refresh-Token")
    if not refresh_header or not refresh_header.lower().startswith("bearer "):
        # TODO custom exception for refresh token
        raise UnauthorizedException()
    # TODO validate
    return refresh_header[7:].strip()


# TODO validate token by public_key
async def validate_access_token(access_token: str) -> bool:
    return True


async def get_authenticated_cognito_service(access_token: str = Depends(get_access_token)):
    cognito_service = injector.resolve(CognitoServiceInterface)
    cognito_service.set_access_token(access_token)
    return cognito_service


async def get_basic_cognito_service():
    cognito_service = injector.resolve(CognitoServiceInterface)
    return cognito_service
