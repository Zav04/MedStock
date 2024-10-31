from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DBMEDSTOCK_PASSWORD = os.getenv('DBMEDSTOCK_PASSWORD')
DBMEDSTOCK_HOST = os.getenv('DBMEDSTOCK_HOST')
DBMEDSTOCK_PORT = os.getenv('DBMEDSTOCK_PORT')
DBMEDSTOCK_USER = os.getenv('DBMEDSTOCK_USER')
DBMEDSTOCK_NAME = os.getenv('DBMEDSTOCK_DB_NAME')

URL_DATABASE_DBMEDSTOCK = f'postgresql://{DBMEDSTOCK_USER}:{DBMEDSTOCK_PASSWORD}@{DBMEDSTOCK_HOST}:{int(DBMEDSTOCK_PORT)}/{DBMEDSTOCK_NAME}'

engine_MEDSTOCK = create_engine(URL_DATABASE_DBMEDSTOCK)
SessionLocal_MEDSTOCK = sessionmaker(autocommit=False, autoflush=False, bind=engine_MEDSTOCK)
Base_MEDSTOCK = declarative_base()
