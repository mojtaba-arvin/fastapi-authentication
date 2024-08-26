import logging
import httpx
from abc import ABC, abstractmethod
from functools import wraps
from typing import Optional, Callable, Type, Any
from dataclasses import dataclass, field
from app.api.models.auth_models import (
    LoginRequest, LoginResponse, SignUpRequest, SignUpResponse,
    ConfirmSignUpRequest, ConfirmSignUpResponse, ResendConfirmationCodeRequest,
    ResendConfirmationCodeResponse, TokenRefreshRequest, TokenRefreshResponse,
    ChangePasswordRequest, ChangePasswordResponse, ForgotPasswordRequest,
    ForgotPasswordResponse, ConfirmForgotPasswordRequest, ConfirmForgotPasswordResponse,
    UpdateUserAttributesRequest, UpdateUserAttributesResponse
)


class CognitoServiceInterface(ABC):

    @abstractmethod
    async def login(self, request: LoginRequest) -> LoginResponse:
        """
        Asynchronously handles user login.

        Args:
            request (LoginRequest): The login request object.

        Returns:
            LoginResponse: The response containing authentication tokens.
        """
        pass

    @abstractmethod
    async def sign_up(self, request: SignUpRequest) -> SignUpResponse:
        """
        Asynchronously handles user sign-up.

        Args:
            request (SignUpRequest): The sign-up request object.

        Returns:
            SignUpResponse: The response with sign-up result and user information.
        """
        pass

    @abstractmethod
    async def confirm_sign_up(self, request: ConfirmSignUpRequest) -> ConfirmSignUpResponse:
        """
        Asynchronously confirms user sign-up.

        Args:
            request (ConfirmSignUpRequest): The confirm sign-up request object.

        Returns:
            ConfirmSignUpResponse: The response indicating success of confirmation.
        """
        pass

    @abstractmethod
    async def resend_confirmation_code(self, request: ResendConfirmationCodeRequest) -> ResendConfirmationCodeResponse:
        """
        Asynchronously resends the confirmation code.

        Args:
            request (ResendConfirmationCodeRequest): The request object for resending code.

        Returns:
            ResendConfirmationCodeResponse: The response confirming code resending.
        """
        pass

    @abstractmethod
    async def refresh_token(self, request: TokenRefreshRequest) -> TokenRefreshResponse:
        """
        Asynchronously refreshes authentication tokens.

        Args:
            request (TokenRefreshRequest): The token refresh request object.

        Returns:
            TokenRefreshResponse: The response containing new access and ID tokens.
        """
        pass

    @abstractmethod
    async def change_password(self, request: ChangePasswordRequest) -> ChangePasswordResponse:
        """
        Asynchronously changes user password.

        Args:
            request (ChangePasswordRequest): The request object for password change.

        Returns:
            ChangePasswordResponse: The response indicating success of the password change.
        """
        pass

    @abstractmethod
    async def forgot_password(self, request: ForgotPasswordRequest) -> ForgotPasswordResponse:
        """
        Asynchronously handles forgot password requests.

        Args:
            request (ForgotPasswordRequest): The request object for initiating password reset.

        Returns:
            ForgotPasswordResponse: The response confirming the password reset request.
        """
        pass

    @abstractmethod
    async def confirm_forgot_password(self, request: ConfirmForgotPasswordRequest) -> ConfirmForgotPasswordResponse:
        """
        Asynchronously confirms forgot password request.

        Args:
            request (ConfirmForgotPasswordRequest): The request object for confirming password reset.

        Returns:
            ConfirmForgotPasswordResponse: The response indicating success of password reset confirmation.
        """
        pass

    @abstractmethod
    async def update_user_attributes(self, request: UpdateUserAttributesRequest) -> UpdateUserAttributesResponse:
        """
        Asynchronously updates user attributes.

        Args:
            request (UpdateUserAttributesRequest): The request object for updating user attributes.

        Returns:
            UpdateUserAttributesResponse: The response confirming the update of user attributes.
        """
        pass


@dataclass
class CognitoService(CognitoServiceInterface):
    """
    Implements CognitoServiceInterface to interact with AWS Cognito asynchronously.
    Provides methods for authentication, user management, and attribute updates.
    """

    client: Optional[httpx.AsyncClient] = field(default=None)
    base_url: Optional[str] = field(default=None)
    basic_credentials: Optional[str] = field(default=None)
    access_token: Optional[str] = field(default=None)
    timeout: float = field(default=10.0)

    logger = logging.getLogger(__name__)

    def __post_init__(self):
        if self.client is None:
            self.client = httpx.AsyncClient(timeout=httpx.Timeout(self.timeout))

    def set_access_token(self, access_token: str):
        """
        Sets the access token for the service.

        Args:
            access_token (str): The access token to set.
        """
        self.access_token = access_token

    @staticmethod
    def log_sensitive_data_remover(data: dict) -> dict:
        """
        Masks sensitive information in the data dictionary.

        Args:
            data (dict): The dictionary containing sensitive information.

        Returns:
            dict: The dictionary with sensitive information masked.
        """
        sensitive_keys = ['password', 'access_token', 'refresh_token', 'id_token']
        return {key: '***' if key in sensitive_keys else value for key, value in data.items()}

    @staticmethod
    def bearer_auth(func: Callable) -> Callable:
        """
        Decorator for adding Bearer Authorization headers.

        Args:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The decorated function with Bearer Authorization headers.
        """
        @wraps(func)
        async def wrapper(cls: 'CognitoService', *args, **kwargs) -> Any:
            headers = {
                "Authorization": f"Bearer {cls.access_token}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            kwargs['headers'] = headers
            return await func(cls, *args, **kwargs)
        return wrapper

    @staticmethod
    def basic_auth(func: Callable) -> Callable:
        """
        Decorator for adding Basic Authorization headers.

        Args:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The decorated function with Basic Authorization headers.
        """
        @wraps(func)
        async def wrapper(cls: 'CognitoService', *args, **kwargs) -> Any:
            headers = {
                "Authorization": f"Basic {cls.basic_credentials}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            kwargs['headers'] = headers
            return await func(cls, *args, **kwargs)
        return wrapper

    @staticmethod
    def call_api(path: str, response_model: Type[Any]) -> Callable:
        """
        Decorator for making API calls and processing responses.

        Args:
            path (str): The API endpoint path.
            response_model (Type[Any]): The model to parse the response into.

        Returns:
            Callable: The decorated function for API calls.
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(cls: 'CognitoService', *args, **kwargs) -> Any:
                url = f"{cls.base_url}/{path}"
                payload = args[0].dict()

                try:
                    safe_payload = cls.log_sensitive_data_remover(payload)
                    cls.logger.info(f"Request to {url} with payload: {safe_payload}")

                    response = await cls.client.post(url, json=payload, headers=kwargs.get('headers'))

                    return await cls._process_response(response, response_model)
                except Exception as e:
                    cls.logger.error(f"API call to {url} failed: {str(e)}")
                    raise e
                finally:
                    await cls.client.aclose()
            return wrapper
        return decorator

    async def close(self):
        """
        Closes the HTTP client and releases resources.
        """
        if self.client is not None:
            await self.client.aclose()

    async def _process_response(self, response: httpx.Response, response_model: Type[Any]) -> Any:
        """
        Processes the API response, handling errors and converting to the response model.

        Args:
            response (httpx.Response): The HTTP response object.
            response_model (Type[Any]): The model to parse the response into.

        Returns:
            Any: The parsed response model instance.
        """
        try:
            response_json = await response.json()
        except ValueError as e:
            self.logger.error(f"JSON decode error: {str(e)}")
            self.logger.error(f"Response content: {response.text}")
            response.raise_for_status()
            raise e

        safe_response_data = CognitoService.log_sensitive_data_remover(response_json)
        self.logger.info(f"Response: {safe_response_data}")

        response.raise_for_status()
        return response_model(**response_json)

    @basic_auth
    @call_api(path="login", response_model=LoginResponse)
    async def login(self, request: LoginRequest) -> LoginResponse:
        pass

    @basic_auth
    @call_api(path="signUp", response_model=SignUpResponse)
    async def sign_up(self, request: SignUpRequest) -> SignUpResponse:
        pass

    @basic_auth
    @call_api(path="confirmSignUp", response_model=ConfirmSignUpResponse)
    async def confirm_sign_up(self, request: ConfirmSignUpRequest) -> ConfirmSignUpResponse:
        pass

    @basic_auth
    @call_api(path="resendConfirmationCode", response_model=ResendConfirmationCodeResponse)
    async def resend_confirmation_code(self, request: ResendConfirmationCodeRequest) -> ResendConfirmationCodeResponse:
        pass

    @basic_auth
    @call_api(path="refreshToken", response_model=TokenRefreshResponse)
    async def refresh_token(self, request: TokenRefreshRequest) -> TokenRefreshResponse:
        pass

    @bearer_auth
    @call_api(path="changePassword", response_model=ChangePasswordResponse)
    async def change_password(self, request: ChangePasswordRequest) -> ChangePasswordResponse:
        pass

    @basic_auth
    @call_api(path="forgotPassword", response_model=ForgotPasswordResponse)
    async def forgot_password(self, request: ForgotPasswordRequest) -> ForgotPasswordResponse:
        pass

    @basic_auth
    @call_api(path="confirmForgotPassword", response_model=ConfirmForgotPasswordResponse)
    async def confirm_forgot_password(self, request: ConfirmForgotPasswordRequest) -> ConfirmForgotPasswordResponse:
        pass

    @bearer_auth
    @call_api(path="updateUserAttributes", response_model=UpdateUserAttributesResponse)
    async def update_user_attributes(self, request: UpdateUserAttributesRequest) -> UpdateUserAttributesResponse:
        pass
