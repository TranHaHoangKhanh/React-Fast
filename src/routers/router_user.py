from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.database import get_session
from src.db.redis import add_jti_to_blocklist

from src.utils.dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.schemas.user_schemas import UserCreateModel, UserModel, UserLoginModel, UserBooksModel
from src.services.user_services import UserService
from src.utils.pwd_hash import create_access_token, decode_token, verify_password

from src.core.config import settings


user_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["users"]
)
user_service = UserService()
role_checker = RoleChecker(["admin","user"])


REFRESH_TOKEN_EXPIRY = settings.REFRESH_TOKEN_EXPIRY


# Bearer Token


@user_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User with email already exists")

    new_user = await user_service.create_user(user_data, session)

    return new_user


@user_router.post("/login")
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
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email or Password"
    )


@user_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'])

        return JSONResponse(content={"access_token": new_access_token})
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid or expired token"
                        )
    
@user_router.get("/me", response_model=UserBooksModel)
async def get_current_user(user = Depends(get_current_user), _: bool = Depends(role_checker)):
    return user


@user_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    
    jti = token_details['jti']
    
    await add_jti_to_blocklist(jti)
    
    return JSONResponse(
        content={
            "message": "Logged out successfully"
        },
        status_code=status.HTTP_200_OK
    )