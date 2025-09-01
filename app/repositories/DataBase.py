from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # Que hace declarative Base? Dice que es un modelo de DB
from sqlalchemy.engine import URL
#from psycopg2 import connect, sql
import os
from dotenv import load_dotenv

load_dotenv()
passwordDB = os.getenv("passwordDB")

"""url = URL.create(
    drivername="postgresql",
    username="postgres",
    password=passwordDB,
    host="localhost",
    port=5432,
    database="MIT" # Cambiar por el nombre de la base de datos
)"""

DB_URL = "sqlite:///./DBase.db"  #Debe protegerse la URL de la DB?

Engine = create_engine(DB_URL)

Session = sessionmaker(autocommit=False,autoflush=False,bind=Engine)
DBase = declarative_base()

def Get_db(): #Funcion que crea una sesion de la DB
    DB = Session()
    try:
      yield DB
    finally:
      DB.close() #Para siempre cerrar la DB luego de usarla