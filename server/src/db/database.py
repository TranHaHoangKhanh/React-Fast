from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from src.core.config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"



engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind=engine )

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        

while True:

    try:
        conn = psycopg2.connect(host= f'{settings.POSTGRES_HOSTNAME}', database= f'{settings.POSTGRES_DB}', user= f'{settings.POSTGRES_USER}', 
                                password = f'{settings.POSTGRES_PASSWORD}', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfully established!!!")
        break
    except Exception as error:
        print("Connecting to database failed!!!!")
        print("Error:", error)   
        time.sleep(2)
        