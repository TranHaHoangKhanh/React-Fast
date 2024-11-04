from fastapi import APIRouter

from src.schema.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from src.service.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(register_body: RegisterSchema):
    await AuthService.register_service(register_body)
    return ResponseSchema(detail="Successfully save data!")


@router.post("/login", response_model=ResponseSchema)
async def login(request_body: LoginSchema):
    token = await AuthService.login_service(request_body)
    return ResponseSchema(detail="Successfully login!", result={"token_type": "Bearer", "access_token": token})


@router.post("/forgot-password", response_model=ResponseSchema, response_model_exclude_none=True)
async def forgot_password(request_body: ForgotPasswordSchema):
    await AuthService.forgot_password_service(request_body)
    return ResponseSchema(detail="Successfully updated data!")
