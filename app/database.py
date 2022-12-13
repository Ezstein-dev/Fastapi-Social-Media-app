from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
from psycopg2._psycopg import cursor
from psycopg2.extras import RealDictCursor
import time
import psycopg2
from .config import settings
import sqlalchemy
import pandas
from sqlalchemy.sql import func,select, literal_column
import functools
from .config import settings


 
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db(): 
    db = SessionLocal() 
    try: 
        yield db 
        print ("Database connection was successfull")
    finally: db.close()



# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#         password='Earlfrosh', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print ("Database connection was successfull")
#         break
#     except Exception as error:
#         print ("Connecting to database failed")
#         print ("Error: ", error)
#         time.sleep(3)