"""
GraphQL resolvers for user-related mutations using Ariadne.

This module defines resolvers for GraphQL mutations related to user authentication and management,
including login, sign-up, password management, and user attribute updates.
"""

from ariadne import MutationType
from fastapi import Depends
from app.services.aws.cognito.auth import CognitoServiceInterface
from app.api.dependencies.auth import (
    get_refresh_token, get_authenticated_cognito_service,
    get_basic_cognito_service
)
from app.api.models.auth_models import (
    LoginRequest, LoginResponse, SignUpRequest, SignUpResponse, ConfirmSignUpRequest,
    ConfirmSignUpResponse, ResendConfirmationCodeRequest, ResendConfirmationCodeResponse,
    TokenRefreshRequest, TokenRefreshResponse, ChangePasswordRequest, ChangePasswordResponse,
    ForgotPasswordRequest, ForgotPasswordResponse, ConfirmForgotPasswordRequest,
    ConfirmForgotPasswordResponse, UpdateUserAttributesRequest, UpdateUserAttributesResponse
)

# Define the MutationType instance for GraphQL
mutation = MutationType()


@mutation.field("login")
async def resolve_login(
        _, info, username: str, password: str,
        cognito_service: CognitoServiceInterface = Depends(get_basic_cognito_service)
) -> LoginResponse:
    """
    Handles the login mutation for user authentication.

    This resolver authenticates a user using their username and password and
    returns the corresponding authentication tokens.

    Args:
        _: Root value, not used.
        info: GraphQL context.
        username (str): User's username.
        password (str): User's password.
        cognito_service (CognitoServiceInterface, optional): The Cognito service instance.

    Returns:
        LoginResponse: A Pydantic model containing login-related tokens.
    """
    request = LoginRequest(username=username, password=password)
    return await cognito_service.login(request)


@mutation.field("signUp")
async def resolve_sign_up(
        _, info, username: str, password: str, email: str, phone_number: str = None,
        given_name: str = None, family_name: str = None,
        cognito_service: CognitoServiceInterface = Depends(get_basic_cognito_service)
) -> SignUpResponse:
    """
    Handles the signUp mutation for new user registration.

    This resolver registers a new user in the Cognito service with the provided
    username, password, and optional personal information.

    Args:
        _: Root value, not used.
        info: GraphQL context.
        username (str): Desired username for the new account.
        password (str): Desired password for the new account.
        email (str): Email address of the new user.
        phone_number (str, optional): Phone number of the new user.
        given_name (str, optional): Given name of the new user.
        family_name (str, optional): Family name of the new user.
        cognito_service (CognitoServiceInterface, optional): The Cognito service instance.

    Returns:
        SignUpResponse: Contains the sign-up status and user subscription details.
    """
    request = SignUpRequest(
        username=username, password=password, email=email,
        phone_number=phone_number, given_name=given_name, family_name=family_name
    )
    return await cognito_service.sign_up(request)


@mutation.field("confirmSignUp")
async def resolve_confirm_sign_up(
        _, info, username: str, confirmation_code: str,
        cognito_service: CognitoServiceInterface = Depends(get_basic_cognito_service)
) -> ConfirmSignUpResponse:
    """
    Handles the confirmSignUp mutation to confirm user registration.

    This resolver confirms a new user's sign-up using the confirmation code
    sent to the user, completing the registration process.

    Args:
        _: Root value, not used.
        info: GraphQL context.
        username (str): The username of the user to confirm.
        confirmation_code (str): The confirmation code received by the user.
        cognito_service (CognitoServiceInterface, optional): The Cognito service instance.

    Returns:
        ConfirmSignUpResponse: A Pydantic model containing the result of the confirmation process.
    """
    request = ConfirmSignUpRequest(username=username, confirmation_code=confirmation_code)
    return await cognito_service.confirm_sign_up(request)


@mutation.field("resendConfirmationCode")
async def resolve_resend_confirmation_code(
        _, info, username: str,
        cognito_service: CognitoServiceInterface = Depends(get_basic_cognito_service)
) -> ResendConfirmationCodeResponse:
    """
    Handles the resendConfirmationCode mutation to resend the confirmation code.

    This resolver resends the confirmation code to the user, which is necessary
    if the user did not receive or lost the original code.

    Args:
        _: Root value, not used.
        info: GraphQL context.
        username (str): The username of the user requesting the code resend.
        cognito_service (CognitoServiceInterface, optional): The Cognito service instance.

    Returns:
        ResendConfirmationCodeResponse: A Pydantic model containing the result of the resend operation.
    """
    request = ResendConfirmationCodeRequest(username=username)
    return await cognito_service.resend_confirmation_code(request)


@mutation.field("refreshToken")
async def resolve_refresh_token(
        _, info, refresh_token: str = Depends(get_refresh_token),
        cognito_service: CognitoServiceInterface = Depends(get_basic_cognito_service)
) -> TokenRefreshResponse:
    """
    Handles the refreshToken mutation to refresh authentication tokens.

    This resolver uses the provided refresh token to obtain new authentication
    tokens (access and ID tokens) from the Cognito service.

    Args:
        _: Root value, not used.
        info: GraphQL context.
        refresh_token (str): The refresh token to be used for getting new tokens.
        cognito_service (CognitoServiceInterface, optional): The Cognito service instance.

    Returns:
        TokenRefreshResponse: A Pydantic model with new access and ID tokens.
    """
    request = TokenRefreshRequest(refresh_token=refresh_token)
    return await cognito_service.refresh_token(request)


@mutation.field("changePassword")
async def resolve_change_password(
        _, info, previous_password: str, proposed_password: str,
        cognito_service: CognitoServiceInterface = Depends(get_authenticated_cognito_service)
) -> ChangePasswordResponse:
    """
    Handles the changePassword mutation for updating the user's password.

    This resolver allows an authenticated user to change their password by
    providing the current password and a new password.

    Args:
        _: Root value, not used.
        info: GraphQL context.
        previous_password (str): The user's current password.
        proposed_password (str): The new password the user wishes to set.
        cognito_service (CognitoServiceInterface, optional): The Cognito service instance.

    Returns:
        ChangePasswordResponse: A Pydantic model containing the result of the password change operation.
    """
    request = ChangePasswordRequest(previous_password=previous_password, proposed_password=proposed_password)
    return await cognito_service.change_password(request)


@mutation.field("forgotPassword")
async def resolve_forgot_password(
        _, info, username: str,
        cognito_service: CognitoServiceInterface = Depends(get_basic_cognito_service)
) -> ForgotPasswordResponse:
    """
    Handles the forgotPassword mutation to initiate the password reset process.

    This resolver starts the password reset process for a user by generating a
    verification code sent to the user's registered email or phone number.

    Args:
        _: Root value, not used.
        info: GraphQL context.
        username (str): The username of the user requesting the password reset.
        cognito_service (CognitoServiceInterface, optional): The Cognito service instance.

    Returns:
        ForgotPasswordResponse: A Pydantic model containing the result of the forgot password operation.
    """
    request = ForgotPasswordRequest(username=username)
    return await cognito_service.forgot_password(request)


@mutation.field("confirmForgotPassword")
async def resolve_confirm_forgot_password(
        _, info, username: str, confirmation_code: str, new_password: str,
        cognito_service: CognitoServiceInterface = Depends(get_basic_cognito_service)
) -> ConfirmForgotPasswordResponse:
    """
    Handles the confirmForgotPassword mutation to confirm the password reset.

    This resolver completes the password reset process by confirming the new
    password using the verification code sent to the user.

    Args:
        _: Root value, not used.
        info: GraphQL context.
        username (str): The username of the user confirming the password reset.
        confirmation_code (str): The verification code sent to the user.
        new_password (str): The new password to be set for the user.
        cognito_service (CognitoServiceInterface, optional): The Cognito service instance.

    Returns:
        ConfirmForgotPasswordResponse: A Pydantic model containing the result of the password reset confirmation.
    """
    request = ConfirmForgotPasswordRequest(
        username=username, confirmation_code=confirmation_code, new_password=new_password
    )
    return await cognito_service.confirm_forgot_password(request)


@mutation.field("updateUserAttributes")
async def resolve_update_user_attributes(
        _, info, attributes: list,
        cognito_service: CognitoServiceInterface = Depends(get_authenticated_cognito_service)
) -> UpdateUserAttributesResponse:
    """
    Handles the updateUserAttributes mutation to update user attributes.

    This resolver allows an authenticated user to update their profile
    attributes such as name, email, or phone number.

    Args:
        _: Root value, not used.
        info: GraphQL context.
        attributes (list): List of attributes to be updated for the user.
        cognito_service (CognitoServiceInterface, optional): The Cognito service instance.

    Returns:
        UpdateUserAttributesResponse: A Pydantic model containing the result of the user attributes update.
    """
    request = UpdateUserAttributesRequest(attributes=attributes)
    return await cognito_service.update_user_attributes(request)
