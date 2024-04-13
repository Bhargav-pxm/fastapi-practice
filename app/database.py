# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# * This FILE is used to setup connection between SQL ALCHEMY and POSTGRES


#! Function to use the DB in main.py file
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
#! Database connection using RAQ SQL(writing queries)
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="bhargav6",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("database connected!!!")
        break
    except Exception as error:
        print("Failed to connect to Db")
        print("error is :", error)
        time.sleep(2)"""
