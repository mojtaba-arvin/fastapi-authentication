from http import HTTPStatus
from typing import Optional


class ErrorDescriptor:
    """
    A class that represents the details of an error.

    Attributes:
        code (str): A unique error code.
        message (str): A user-friendly message describing the error.
        http_status (HTTPStatus): The HTTP status code associated with the error.
        tracking_code (Optional[str]): An optional tracking code for further support.
    """

    def __init__(self, code: str, message: str, http_status: HTTPStatus, tracking_code: Optional[str] = None):
        """
        Initializes an instance of ErrorDescriptor.

        Args:
            code (str): A unique error code.
            message (str): A user-friendly message describing the error.
            http_status (HTTPStatus): The HTTP status code for the error.
            tracking_code (Optional[str]): An optional tracking code for further support.
        """
        self.code = code
        self.message = message
        self.http_status = http_status
        self.tracking_code = tracking_code


class ErrorCodes:
    """
    A class that defines and maps various error codes to their corresponding ErrorDescriptor instances.
    """

    # General error codes (1000-1999)
    INTERNAL_ERROR = ErrorDescriptor(
        code="1000",
        message="An unexpected error occurred. Please try again later.",
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR
    )
    INVALID_REQUEST = ErrorDescriptor(
        code="1001",
        message="The request was invalid. Please check your input.",
        http_status=HTTPStatus.BAD_REQUEST
    )
    SERVICE_UNAVAILABLE = ErrorDescriptor(
        code="1002",
        message="Service is temporarily unavailable. Please try again later.",
        http_status=HTTPStatus.SERVICE_UNAVAILABLE
    )

    # Authentication-related error codes (2000-2999)
    AUTHENTICATION_FAILED = ErrorDescriptor(
        code="2000",
        message="Authentication failed. Please check your credentials.",
        http_status=HTTPStatus.UNAUTHORIZED
    )
    EMAIL_NOT_CONFIRMED = ErrorDescriptor(
        code="2001",
        message="Your email address has not been confirmed.",
        http_status=HTTPStatus.FORBIDDEN
    )
    USER_NOT_FOUND = ErrorDescriptor(
        code="2002",
        message="The specified user does not exist.",
        http_status=HTTPStatus.NOT_FOUND
    )
    PASSWORD_TOO_SHORT = ErrorDescriptor(
        code="2003",
        message="The password provided is too short.",
        http_status=HTTPStatus.BAD_REQUEST
    )
    PASSWORD_INCORRECT = ErrorDescriptor(
        code="2004",
        message="The password provided is incorrect.",
        http_status=HTTPStatus.UNAUTHORIZED
    )
    TOKEN_EXPIRED = ErrorDescriptor(
        code="2005",
        message="The session has expired. Please log in again.",
        http_status=HTTPStatus.UNAUTHORIZED
    )
    CODE_MISMATCH = ErrorDescriptor(
        code="2006",
        message="The confirmation code does not match.",
        http_status=HTTPStatus.BAD_REQUEST
    )
    UNAUTHORIZED = ErrorDescriptor(
        code="2007",
        message="You are not authorized to perform this action.",
        http_status=HTTPStatus.UNAUTHORIZED
    )
    USER_ALREADY_EXISTS = ErrorDescriptor(
        code="2008",
        message="A user with this information already exists.",
        http_status=HTTPStatus.CONFLICT
    )


class ServiceUnavailableSupportCodes:
    """
    A class to manage support codes for third-party errors that result in service unavailability (error code:1002).
    """

    # AWS Cognito related errors
    COGNITO_REQUEST_LIMIT_EXCEEDED = "COG-REQ-0001"
    """
    Exception raised when the request limit is exceeded.

    Reference:
        https://docs.aws.amazon.com/cognito/latest/developerguide/troubleshooting.html#http-503-error
    """

    COGNITO_LIMIT_EXCEEDED = "COG-LIM-0002"
    """
    Exception raised when a limit is exceeded on AWS Cognito.

    Reference:
        https://docs.aws.amazon.com/cognito/latest/developerguide/troubleshooting.html#http-503-error
    """

    COGNITO_INVALID_PARAMETER = "COG-PAR-0003"
    """
    Exception raised for invalid parameters in AWS Cognito requests.

    Reference:
        https://docs.aws.amazon.com/cognito/latest/developerguide/troubleshooting.html#invalid-parameter-exception
    """

    COGNITO_INTERNAL_ERROR = "COG-INT-0004"
    """
    Exception raised for internal server errors.

    Reference: https://docs.aws.amazon.com/cognitoidentityprovider/latest/APIReference/API_AdminInitiateAuth.html
    """
