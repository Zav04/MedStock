from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DBMEDSTOCK_PASSWORD = os.getenv('DBLOINC_PASSWORD')
DBMEDSTOCK_HOST = os.getenv('DBLOINC_HOST')
DBMEDSTOCK_PORT = os.getenv('DBLOINC_PORT')
DBMEDSTOCK_USER = os.getenv('DBLOINC_USER')
DBMEDSTOCK_NAME = os.getenv('DBLOINC_NAME')

URL_DATABASE_DBMEDSTOCK = f'postgresql://{DBMEDSTOCK_USER}:{DBMEDSTOCK_PASSWORD}@{DBMEDSTOCK_HOST}:{int(DBMEDSTOCK_PORT)}/{DBMEDSTOCK_NAME}'

engine_MEDSTOCK = create_engine(URL_DATABASE_DBMEDSTOCK)
SessionLocal_MEDSTOCK = sessionmaker(autocommit=False, autoflush=False, bind=engine_MEDSTOCK)
Base_MEDSTOCK = declarative_base()
