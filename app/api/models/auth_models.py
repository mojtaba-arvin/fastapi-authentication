from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Dict


class LoginRequest(BaseModel):
    """
    Model for user login request.

    Attributes:
        username (constr(min_length=1, max_length=50)): The user's username.
        password (constr(min_length=6, max_length=128)): The user's password.

    Reference:
        [AWS Cognito InitiateAuth API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_InitiateAuth.html)
    """
    username: constr(min_length=1, max_length=50)
    password: constr(min_length=6, max_length=128)


class LoginResponse(BaseModel):
    """
    Model for user login response.

    Attributes:
        access_token (str): The access token issued after successful authentication.
        token_type (str): Type of the token, typically 'Bearer'. Default is 'Bearer'.
        refresh_token (Optional[str]): Token to refresh the access token.
        id_token (Optional[str]): ID token that contains user claims.

    Reference:
        [AWS Cognito InitiateAuth API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_InitiateAuth.html)
    """
    access_token: str
    token_type: str = "Bearer"
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None


class SignUpRequest(BaseModel):
    """
    Model for user sign-up request.

    Attributes:
        username (constr(min_length=1, max_length=50)): The user's username.
        password (constr(min_length=6, max_length=128)): The user's password.
        email (EmailStr): The user's email address.
        phone_number (Optional[constr(max_length=15)]): The user's phone number (optional).
        given_name (Optional[constr(max_length=50)]): The user's given name (optional).
        family_name (Optional[constr(max_length=50)]): The user's family name (optional).

    Reference:
        [AWS Cognito SignUp API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_SignUp.html)
    """
    username: constr(min_length=1, max_length=50)
    password: constr(min_length=6, max_length=128)
    email: EmailStr
    phone_number: Optional[constr(max_length=15)] = None
    given_name: Optional[constr(max_length=50)] = None
    family_name: Optional[constr(max_length=50)] = None


class SignUpResponse(BaseModel):
    """
    Model for user sign-up response.

    Attributes:
        message (str): Message indicating the result of the sign-up process.
        user_sub (Optional[str]): User ID returned by Cognito after sign-up.

    Reference:
        [AWS Cognito SignUp API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_SignUp.html)
    """
    message: str
    user_sub: Optional[str] = None


class ConfirmSignUpRequest(BaseModel):
    """
    Model for sign-up confirmation request.

    Attributes:
        username (constr(min_length=1, max_length=50)): The user's username.
        confirmation_code (constr(min_length=6, max_length=10)): The confirmation code sent to the user.

    Reference:
        [AWS Cognito ConfirmSignUp API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_ConfirmSignUp.html)
    """
    username: constr(min_length=1, max_length=50)
    confirmation_code: constr(min_length=6, max_length=10)


class ConfirmSignUpResponse(BaseModel):
    """
    Model for sign-up confirmation response.

    Attributes:
        message (str): Message indicating the result of the confirmation process.

    Reference:
        [AWS Cognito ConfirmSignUp API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_ConfirmSignUp.html)
    """
    message: str


class ResendConfirmationCodeRequest(BaseModel):
    """
    Model for resending confirmation code request.

    Attributes:
        username (constr(min_length=1, max_length=50)): The user's username.

    Reference:
        [AWS Cognito ResendConfirmationCode API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_ResendConfirmationCode.html)
    """
    username: constr(min_length=1, max_length=50)


class ResendConfirmationCodeResponse(BaseModel):
    """
    Model for resending confirmation code response.

    Attributes:
        message (str): Message indicating the result of resending the confirmation code.

    Reference:
        [AWS Cognito ResendConfirmationCode API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_ResendConfirmationCode.html)
    """
    message: str


class TokenRefreshRequest(BaseModel):
    """
    Model for token refresh request.

    Attributes:
        refresh_token (constr(min_length=1)): The refresh token used to obtain a new access token.

    Reference:
        [AWS Cognito RefreshToken API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_RefreshToken.html)
    """
    refresh_token: constr(min_length=1)


class TokenRefreshResponse(BaseModel):
    """
    Model for token refresh response.

    Attributes:
        access_token (str): The new access token.
        token_type (str): Type of the token, typically 'Bearer'. Default is 'Bearer'.
        id_token (Optional[str]): New ID token (optional).

    Reference:
        [AWS Cognito RefreshToken API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_RefreshToken.html)
    """
    access_token: str
    token_type: str = "Bearer"
    id_token: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    """
    Model for changing password request.

    Attributes:
        access_token (constr(min_length=1)): Current access token.
        previous_password (constr(min_length=6, max_length=128)): The user's current password.
        proposed_password (constr(min_length=6, max_length=128)): The new password to set.

    Reference:
        [AWS Cognito ChangePassword API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_ChangePassword.html)
    """
    access_token: constr(min_length=1)
    previous_password: constr(min_length=6, max_length=128)
    proposed_password: constr(min_length=6, max_length=128)


class ChangePasswordResponse(BaseModel):
    """
    Model for changing password response.

    Attributes:
        message (str): Message indicating the result of the password change process.

    Reference:
        [AWS Cognito ChangePassword API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_ChangePassword.html)
    """
    message: str


class ForgotPasswordRequest(BaseModel):
    """
    Model for forgot password request.

    Attributes:
        username (constr(min_length=1, max_length=50)): The user's username (or email).

    Reference:
        [AWS Cognito ForgotPassword API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_ForgotPassword.html)
    """
    username: constr(min_length=1, max_length=50)


class ForgotPasswordResponse(BaseModel):
    """
    Model for forgot password response.

    Attributes:
        message (str): Message indicating the result of the forgot password process.

    Reference:
        [AWS Cognito ForgotPassword API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_ForgotPassword.html)
    """
    message: str


class ConfirmForgotPasswordRequest(BaseModel):
    """
    Model for confirming forgot password request.

    Attributes:
        username (constr(min_length=1, max_length=50)): The user's username (or email).
        confirmation_code (constr(min_length=6, max_length=10)): The confirmation code sent to the user.
        new_password (constr(min_length=6, max_length=128)): The new password to set.

    Reference:
        [AWS Cognito ConfirmForgotPassword API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_ConfirmForgotPassword.html)
    """
    username: constr(min_length=1, max_length=50)
    confirmation_code: constr(min_length=6, max_length=10)
    new_password: constr(min_length=6, max_length=128)


class ConfirmForgotPasswordResponse(BaseModel):
    """
    Model for confirming forgot password response.

    Attributes:
        message (str): Message indicating the result of the password reset process.

    Reference:
        [AWS Cognito ConfirmForgotPassword API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_ConfirmForgotPassword.html)
    """
    message: str


class UpdateUserAttributesRequest(BaseModel):
    """
    Model for updating user attributes request.

    Attributes:
        access_token (constr(min_length=1)): Access token to authorize the request.
        attributes (Dict[str, str]): Dictionary of attributes to update.

    Reference:
        [AWS Cognito UpdateUserAttributes API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_UpdateUserAttributes.html)
    """
    access_token: constr(min_length=1)
    attributes: Dict[str, str]


class UpdateUserAttributesResponse(BaseModel):
    """
    Model for updating user attributes response.

    Attributes:
        message (str): Message indicating the result of the update process.

    Reference:
        [AWS Cognito UpdateUserAttributes API](https://docs.aws.amazon.com/cognitoidentitypools/latest/APIReference/API_UpdateUserAttributes.html)
    """
    message: str
