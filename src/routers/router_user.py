from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.database import get_session
from src.db.redis import add_jti_to_blocklist

from src.core.config import settings
from src.utils.dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.schemas.user_schemas import UserBooksModel, UserCreateModel, UserLoginModel, UserModel, EmailModel, PasswordResetRequestModel, PasswordResetConfirmModel
from src.services.user_services import UserService
from src.utils.pwd_hash import create_access_token, verify_password, generate_passwd_hash, create_url_safe_token, decode_url_safe_token
from src.utils.error_handling import (
    UserAlreadyExists,
    UserNotFound,
    InvalidCredentials,
    InvalidToken,
    PasswordNotMatched
)
from src.core.config import settings
from src.utils.mail import mail, create_message
"""
Background tasks for celery
from src.utils.celery_tasks import send_email
"""


user_router = APIRouter(
    prefix='/api/v1/auth',
    tags=["users"]
)
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])


REFRESH_TOKEN_EXPIRY = settings.REFRESH_TOKEN_EXPIRY


# Bearer Token


@user_router.post('/send_mail')
async def send_mail(emails: EmailModel, bg_tasks: BackgroundTasks):
    emails = emails.addresses

    html = "<h1>Welcome to the app</h1>"
    subject = "Welcome to my app"
    
    # send_email.delay(recipients=emails, subject=subject, body=html)
    
    
    message = create_message(recipients=emails, subject=subject, body=html)
    
    bg_tasks.add_task(mail.send_message, message)
    
    return {"message": "Email sent successfully"}


@user_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, bg_tasks: BackgroundTasks, session: AsyncSession = Depends(get_session)):
    """
    Create user account using email, username, first name, last name params
        user_data: UserCreateModel
    """
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})

    link = f"{settings.DOMAIN}/api/v1/auth/verify/{token}"

    html = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email.</p>
    """
    emails = [email]
    
    subject = "Verify your email"
    
    message = create_message(recipients=emails, subject=subject, body=html)
    
    bg_tasks.add_task(message.send_mail, message)
    
    # send_email.delay(recipients=emails, subject=subject, body=html)
    
    return {
        "message": "Account Created! Check email to verify your account",
        "user": new_user
    }


@user_router.get('/verify/{token}')
async def verify_user_token(token: str, session: AsyncSession = Depends(get_session)):

    token_data = decode_url_safe_token(token)

    user_email = token_data.get('email')

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK
        )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@user_router.post('/login')
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):

    print(login_data.email)
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid),
                    "role": user.role
                }
            )

            refresh_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
    raise InvalidCredentials()


@user_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'])

        return JSONResponse(content={"access_token": new_access_token})
    raise InvalidToken()


@user_router.get('/me', response_model=UserBooksModel)
async def get_current_user(user=Depends(get_current_user), _: bool = Depends(role_checker)):
    return user


@user_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):

    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message": "Logged out successfully"
        },
        status_code=status.HTTP_200_OK
    )


@user_router.post('/password-reset-request')
async def password_reset_request(email_data: PasswordResetRequestModel, bg_tasks: BackgroundTasks):
    email = email_data.email

    token = create_url_safe_token({"email": email})

    link = f"{settings.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html = f"""
    <h1>Reset Your Password</h1>
    <p>Please click this <a href="{link}">link</a> to Reset Your Password.</p>
    """

    subject = "Reset Your Password"
    
    message = create_message(recipients=[email], subject=subject, body=html)
    
    bg_tasks.add_task(mail.send_message, message)
    
    # send_email.delay(recipients=[email], subject=subject, body=html)

    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password"},
        status_code=status.HTTP_200_OK
    )


@user_router.post('/password-reset-confirm/{token}')
async def reset_account_password(token: str, password: PasswordResetConfirmModel, session: AsyncSession = Depends(get_session)):

    new_password = password.new_password
    confirm_password = password.confirm_new_password

    if new_password != confirm_password:
        raise PasswordNotMatched()

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        passwd_hash = generate_passwd_hash(new_password)
        await user_service.update_user(user, {"password_hash": passwd_hash}, session)

        return JSONResponse(
            content={"message": "Password reset successfully"},
            status_code=status.HTTP_200_OK
        )

    return JSONResponse(
        content={"message": "Error occured during password reset."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
