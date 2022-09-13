from datetime import time

from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)


BASE=declarative_base()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         connection=psycopg2.connect(host='localhost',database='fastAPI',
#                                     user='postgres',password='saim123',cursor_factory=RealDictCursor)
#         cursor=connection.cursor()
#         print("Database connection was succesfull")
#         break
#     except Exception as error:
#         print(f"Connecting to database failed error : {error}")
#         print("Try again")
#         time.sleep(2)