import logging
import uuid
from datetime import timedelta, datetime
from itsdangerous import URLSafeTimedSerializer

import jwt
from passlib.context import CryptContext
from src.core.config import settings

passwd_context = CryptContext(schemes=['bcrypt'])

ACCESS_TOKEN_EXPIRY = settings.ACCESS_TOKEN_EXPIRY


def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload["user"] = user_data

    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )

    payload["jti"] = str(uuid.uuid4())

    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt= token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        
        return token_data
    
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

serializer = URLSafeTimedSerializer(
        secret_key=settings.JWT_SECRET,
        salt="email-configuration"
)

def create_url_safe_token(data: dict):
    
    token = serializer.dumps(data)
    
    return token

def decode_url_safe_token(token: str):
    try:
        token_data = serializer.loads(token)
        
        return token_data
    
    except Exception as e:
        logging.error(str(e))
