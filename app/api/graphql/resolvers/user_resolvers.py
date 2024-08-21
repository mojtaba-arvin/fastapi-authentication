"""
GraphQL resolvers for user-related mutations using Ariadne.

This module defines the resolvers for GraphQL mutations related to user authentication and management.
"""

from ariadne import MutationType
from app.services.aws.cognito.auth import CognitoService
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
async def resolve_login(_, info, username: str, password: str) -> LoginResponse:
    """
    Resolver for the `login` mutation.

    Args:
        _: Reserved for context, not used here.
        info: GraphQL execution context.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        LoginResponse: A Pydantic model containing login-related tokens.
    """
    request = LoginRequest(username=username, password=password)
    return await CognitoService.login(request)


@mutation.field("signUp")
async def resolve_sign_up(
        _, info, username: str, password: str, email: str, phone_number: str = None,
        given_name: str = None, family_name: str = None
) -> SignUpResponse:
    """
    Resolver for the `signUp` mutation.

    Args:
        _: Reserved for context, not used here.
        info: GraphQL execution context.
        username (str): The username for the new account.
        password (str): The password for the new account.
        email (str): The email address of the new user.
        phone_number (str, optional): The phone number of the new user.
        given_name (str, optional): The given name of the new user.
        family_name (str, optional): The family name of the new user.

    Returns:
        SignUpResponse: A Pydantic model with sign-up result and user subscription identifier.
    """
    request = SignUpRequest(
        username=username, password=password, email=email,
        phone_number=phone_number, given_name=given_name, family_name=family_name
    )
    return await CognitoService.sign_up(request)


@mutation.field("confirmSignUp")
async def resolve_confirm_sign_up(_, info, username: str, confirmation_code: str) -> ConfirmSignUpResponse:
    """
    Resolver for the `confirmSignUp` mutation.

    Args:
        _: Reserved for context, not used here.
        info: GraphQL execution context.
        username (str): The username to confirm sign-up for.
        confirmation_code (str): The confirmation code received by the user.

    Returns:
        ConfirmSignUpResponse: A Pydantic model containing the result of the confirmation process.
    """
    request = ConfirmSignUpRequest(username=username, confirmation_code=confirmation_code)
    return await CognitoService.confirm_sign_up(request)


@mutation.field("resendConfirmationCode")
async def resolve_resend_confirmation_code(_, info, username: str) -> ResendConfirmationCodeResponse:
    """
    Resolver for the `resendConfirmationCode` mutation.

    Args:
        _: Reserved for context, not used here.
        info: GraphQL execution context.
        username (str): The username for which to resend the confirmation code.

    Returns:
        ResendConfirmationCodeResponse: A Pydantic model containing the result of the resend operation.
    """
    request = ResendConfirmationCodeRequest(username=username)
    return await CognitoService.resend_confirmation_code(request)


@mutation.field("refreshToken")
async def resolve_refresh_token(_, info, refresh_token: str) -> TokenRefreshResponse:
    """
    Resolver for the `refreshToken` mutation.

    Args:
        _: Reserved for context, not used here.
        info: GraphQL execution context.
        refresh_token (str): The refresh token to be used for obtaining new tokens.

    Returns:
        TokenRefreshResponse: A Pydantic model with new access and ID tokens.
    """
    request = TokenRefreshRequest(refresh_token=refresh_token)
    return await CognitoService.refresh_token(request)


@mutation.field("changePassword")
async def resolve_change_password(
        _, info, access_token: str, previous_password: str, proposed_password: str
) -> ChangePasswordResponse:
    """
    Resolver for the `changePassword` mutation.

    Args:
        _: Reserved for context, not used here.
        info: GraphQL execution context.
        access_token (str): The access token of the user changing the password.
        previous_password (str): The current password of the user.
        proposed_password (str): The new password proposed by the user.

    Returns:
        ChangePasswordResponse: A Pydantic model containing the result of the password change operation.
    """
    request = ChangePasswordRequest(
        access_token=access_token, previous_password=previous_password, proposed_password=proposed_password
    )
    return await CognitoService.change_password(request)


@mutation.field("forgotPassword")
async def resolve_forgot_password(_, info, username: str) -> ForgotPasswordResponse:
    """
    Resolver for the `forgotPassword` mutation.

    Args:
        _: Reserved for context, not used here.
        info: GraphQL execution context.
        username (str): The username for which to initiate the password reset process.

    Returns:
        ForgotPasswordResponse: A Pydantic model containing the result of the forgot password operation.
    """
    request = ForgotPasswordRequest(username=username)
    return await CognitoService.forgot_password(request)


@mutation.field("confirmForgotPassword")
async def resolve_confirm_forgot_password(
        _, info, username: str, confirmation_code: str, new_password: str
) -> ConfirmForgotPasswordResponse:
    """
    Resolver for the `confirmForgotPassword` mutation.

    Args:
        _: Reserved for context, not used here.
        info: GraphQL execution context.
        username (str): The username for which to confirm the password reset.
        confirmation_code (str): The confirmation code received by the user.
        new_password (str): The new password to set.

    Returns:
        ConfirmForgotPasswordResponse: A Pydantic model containing the result of the password reset confirmation.
    """
    request = ConfirmForgotPasswordRequest(
        username=username, confirmation_code=confirmation_code, new_password=new_password
    )
    return await CognitoService.confirm_forgot_password(request)


@mutation.field("updateUserAttributes")
async def resolve_update_user_attributes(_, info, access_token: str, attributes: list) -> UpdateUserAttributesResponse:
    """
    Resolver for the `updateUserAttributes` mutation.

    Args:
        _: Reserved for context, not used here.
        info: GraphQL execution context.
        access_token (str): The access token of the user updating their attributes.
        attributes (list): A list of attributes to update.

    Returns:
        UpdateUserAttributesResponse: A Pydantic model containing the result of the user attributes update.
    """
    request = UpdateUserAttributesRequest(access_token=access_token, attributes=attributes)
    return await CognitoService.update_user_attributes(request)
