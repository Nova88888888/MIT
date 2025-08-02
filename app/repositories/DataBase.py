from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "sqlite:///./DBase.db"  #Debe protegerse la URL de la DB?

Engine = create_engine(DB_URL)

Session = sessionmaker(autocommit=False,autoflush=False,bind=Engine)
DBase = declarative_base()

def Get_db():
    DB = Session()
    try:
      yield DB
    finally:
      DB.close()