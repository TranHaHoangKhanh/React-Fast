from fastapi import APIRouter, Depends, Security
import sqlalchemy
from src.schema.schema import ResponseSchema, UserProfileSchema
from src.repository.auth_repo import JWTBearer, JWTRepo
from fastapi.security import HTTPAuthorizationCredentials
from src.service.users import UserService


router = APIRouter(
    prefix="/Users", 
    tags=["users"],
    dependencies=[Depends(JWTBearer())]
)

@router.post("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    # Extract username from JWT token
    token = JWTRepo.extract_token(credentials)
    
    # Get user profile data
    result = await UserService.get_user_profile(token['username'])
    if isinstance(result, sqlalchemy.engine.row.RowMapping):
        result = UserProfileSchema(**dict(result))
    # Convert SQLAlchemy result to dict
    return ResponseSchema(detail="Successfully get data!", result=result)