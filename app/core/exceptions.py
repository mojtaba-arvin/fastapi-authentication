from typing import Optional
from fastapi import HTTPException
from app.core.error_codes import ErrorDescriptor, ErrorCodes


class AppException(HTTPException):
    """
    Custom application exception that utilizes ErrorDescriptor for error details.
    """
    error_descriptor = ErrorCodes.INTERNAL_ERROR  # Default descriptor; should be overridden in subclasses.

    def __init__(self, error_descriptor: ErrorDescriptor = None, support_code: Optional[str] = None):
        error_descriptor = error_descriptor or self.error_descriptor
        super().__init__(
            status_code=error_descriptor.http_status,
            detail={
                "code": error_descriptor.code,
                "message": error_descriptor.message,
                "support_code": support_code
            }
        )


# Specific exception classes for different error types
class InternalErrorException(AppException):
    """
    Exception raised for internal server errors.
    """
    error_descriptor = ErrorCodes.INTERNAL_ERROR


class InvalidRequestException(AppException):
    """
    Exception raised for bad request errors.
    """
    error_descriptor = ErrorCodes.INVALID_REQUEST


class ServiceUnavailableException(AppException):
    """
    Exception raised when the service is temporarily unavailable.
    """
    error_descriptor = ErrorCodes.SERVICE_UNAVAILABLE


class AuthenticationFailedException(AppException):
    """
    Exception raised for authentication failures.

    Reference: https://docs.aws.amazon.com/cognitoidentityprovider/latest/APIReference/API_InitiateAuth.html
    """
    error_descriptor = ErrorCodes.AUTHENTICATION_FAILED


class EmailNotConfirmedException(AppException):
    """
    Exception raised when the email address is not confirmed.

    Reference: https://docs.aws.amazon.com/cognitoidentityprovider/latest/APIReference/API_ResendConfirmationCode.html
    """
    error_descriptor = ErrorCodes.EMAIL_NOT_CONFIRMED


class UserNotFoundException(AppException):
    """
    Exception raised when the user is not found.

    Reference: https://docs.aws.amazon.com/cognitoidentityprovider/latest/APIReference/API_AdminGetUser.html
    """
    error_descriptor = ErrorCodes.USER_NOT_FOUND


class PasswordTooShortException(AppException):
    """
    Exception raised when the password is too short.

    Reference: https://docs.aws.amazon.com/cognitoidentityprovider/latest/APIReference/API_SignUp.html
    """
    error_descriptor = ErrorCodes.PASSWORD_TOO_SHORT


class PasswordIncorrectException(AppException):
    """
    Exception raised when the password is incorrect.

    Reference: https://docs.aws.amazon.com/cognitoidentityprovider/latest/APIReference/API_ChangePassword.html
    """
    error_descriptor = ErrorCodes.PASSWORD_INCORRECT


class TokenExpiredException(AppException):
    """
    Exception raised when the token has expired.

    Reference: https://docs.aws.amazon.com/cognitoidentityprovider/latest/APIReference/API_RespondToAuthChallenge.html
    """
    error_descriptor = ErrorCodes.TOKEN_EXPIRED


class CodeMismatchException(AppException):
    """
    Exception raised when the confirmation code does not match.

    Reference: https://docs.aws.amazon.com/cognitoidentityprovider/latest/APIReference/API_ConfirmSignUp.html
    """
    error_descriptor = ErrorCodes.CODE_MISMATCH


class UnauthorizedException(AppException):
    """
    Exception raised when a user is unauthorized to perform an action.

    Reference: https://docs.aws.amazon.com/cognitoidentityprovider/latest/APIReference/API_InitiateAuth.html
    """
    error_descriptor = ErrorCodes.UNAUTHORIZED


class UserAlreadyExistsException(AppException):
    """
    Exception raised when a user with the same credentials already exists.

    Reference: https://docs.aws.amazon.com/cognitoidentityprovider/latest/APIReference/API_SignUp.html
    """
    error_descriptor = ErrorCodes.USER_ALREADY_EXISTS
