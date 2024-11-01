from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_HOSTNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    

    class Config:
        env_file = ".env"


settings = Settings()

