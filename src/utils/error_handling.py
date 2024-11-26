from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


class BookException(Exception):
    """This is the base class for all book errors."""

    pass


class InvalidToken(BookException):
    """User has provided an invalid or expired token."""

    pass


class RevokedToken(BookException):
    """User has provided a token that has been revoked."""

    pass


class AccessTokenRequired(BookException):
    """User has provided a refresh token when an access token is needed."""

    pass


class RefreshTokenRequired(BookException):
    """User has provided an access token when a refresh token is needed."""

    pass


class UserAlreadyExists(BookException):
    """User has provided an email for a user who exists during sign up."""

    pass


class InvalidCredentials(BookException):
    """User has provided wrong email or password during log in."""

    pass


class InsufficientPermission(BookException):
    """User has provided an email for a user who exists during sign up."""

    pass


class BookNotFound(BookException):
    """Book not found"""

    pass


class ReviewNotFound(BookException):
    """Review not found"""

    pass


class ReviewNotDeleted(BookException):
    """Cannot delete this review."""

    pass


class ReviewError(BookException):
    """Oops... somethig went wrong!"""

    pass


class TagServerError(BookException):
    """Something went wrong"""

    pass


class TagNotFound(BookException):
    """Tag not found"""

    pass


class TagAlreadyExists(BookException):
    """Tag already exists"""

    pass


class UserNotFound(BookException):
    """User not found"""

    pass


class AccountNotVerified(BookException):
    """Account not yet verified"""

    pass

class PasswordNotMatched(BookException):
    """Passwords do not match"""
    
    pass


def create_exception_handler(status_code: int, initial_detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BookException):

        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists"
            }
        )
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found"
            }
        )
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email or Password",
                "error_code": "invalid_email_or_password"
            }
        )
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or expired",
                "resoulution": "Please get new token",
                "error_code": "invalid_token"
            }
        )
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is valid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked"
            }
        )
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required"
            }
        )
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get a refresh token",
                "error_code": "refresh_token_required"
            }
        )
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permission to perform this action",
                "error_code": "insufficient_permission"
            }
        )
    )
    
    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book not found",
                "error_code": "book_not_found"
            }
        )
    )
    
    app.add_exception_handler(
        ReviewNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Review not found",
                "error_code": "review_not_found"
            }
        )
    )
    
    app.add_exception_handler(
        ReviewNotDeleted,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Cannot delete this review",
                "error_code": "review_not_deleted"
            }
        )
    )
    
    app.add_exception_handler(
        ReviewError,
        create_exception_handler(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            initial_detail={
                "message": "Oops... something went wrong!",
                "error_code": "review_error"
            }
        )
    )

    app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Tag not found",
                "error_code": "tag_not_found"
            }
        )
    )

    app.add_exception_handler(
        TagAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Tag already exists",
                "error_code": "tag_exists"
            }
        )
    )
    
    app.add_exception_handler(
        TagServerError,
        create_exception_handler(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            initial_detail={
                "message": "Something went wrong",
                "error_code": "tag_server_error"
            }
        )
    )
    
    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account Not Verified",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details"
            }
        )
    )
    
    app.add_exception_handler(
        PasswordNotMatched,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Passwords do not match",
                "error_code": "password_not_matched"
            }
        )
    )
    
    
    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong!",
                "error_code": "server_error"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong!",
                "error_code": "server_error"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
