from app.schemes import Schemas as S
from app.repositories.Repo import Repositorio

from email_validator import validate_email, EmailNotValidError
from smtplib import SMTP_SSL
from email.message import EmailMessage
from sqlalchemy.orm import Session
import pandas as pd
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime,timedelta, timezone
import jwt
from jwt import PyJWTError
import os
from dotenv import load_dotenv

load_dotenv()
passwordE = os.getenv("password")
SECRET = os.getenv("SECRET")
crypt = CryptContext(schemes=["bcrypt"])

class Email_Serv(): 
    def __init__(self):
        self.email = "mit.prueba@hotmail.com"
        self.password = passwordE
        self.Repo = Repositorio()
    
    def Notificacion(self, user: S.User, message: str): #Envia una notificacion a un Usuario
        Notificacc = EmailMessage()
        Notificacc["Subject"] = "MIT" 
        Notificacc["From"] = self.email 
        Notificacc["To"] = user.email
        Notificacc.set_content(message)
        with SMTP_SSL("smtp.gmail.com", 465) as conn:
          conn.login(self.email, passwordE)
          conn.send_message(Notificacc)

    def ValEmail(self, email:str) -> bool:
        """
        Chequea si un string es un correo, que existe y se le puedan mandar mensajes
        """
        valid = validate_email(email, check_deliverability=True)
        if valid == EmailNotValidError:
              raise False
        else:
              return True




    def Registro(self, user:S.User_DB, db:Session) -> HTTPException | str:
        if self.Repo.readUs(db, user.email):
            raise HTTPException(status_code =400,detail="Ya existe un usuario como este")

        email_val: bool = self.ValEmail(user.email)

        if not email_val:
            raise HTTPException(status_code= 400,detail="El email es invalido")
            raise HTTPException(status_code= 400,detail="El email es invalido")

        #passwordEncode = jwt.encode({user.password}, SECRET,algorithm=["HS256"])
        crypted_password = crypt.hash(user.password, scheme="bcrypt")
        user.password = crypted_password
        self.Repo.createUs(user, db)
        return "Se ha registrado correctamente"




    #[]
    def LogIn(self, user: OAuth2PasswordRequestForm, db: Session) -> HTTPException | dict:
      
      if not self.Repo.readUs(db, user.username): #Verificamos que exista    Quitar?
            raise HTTPException(status_code =404,detail="El usuario no existe")

      User_DB = self.Repo.readUs(db, user.username) #Ya que existe pedimos su información 

      if not crypt.verify(secret=user.password, hash=User_DB.password): #Comprobamos la contraseña
         raise HTTPException(status_code=400 , detail="Contraseña Incorrecta")

      if not User_DB.email == user.username: #Comprobamos el email
        raise HTTPException(status_code=400 , detail="Nombre Incorrecto")

      access_token = {"sub": user.username,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=5)}

      return {"access_token": jwt.encode(access_token, SECRET, algorithm="HS256"), "token_type": "bearer"}  

    def Bearer(self, Token: str, db: Session) -> S.User_DB | HTTPException:
        try:
          JWT = jwt.decode(Token, SECRET, algorithms=["HS256"]).get("sub")
          if JWT == None:
                 raise HTTPException(status_code=401 , detail="Credencial Invalida") #El token no tiene el atributo user
        except PyJWTError:
                raise HTTPException(status_code=401 , detail="Credencial Invalida")#El Token no puede desencriptarse con las llaves
        
        user = self.Repo.readUs(db, JWT)                        #Traemos el Usuario de Base de Datos, porque existe "user" y pudo desencriptarse
        if not user:                                                 #Si el usuario no existe ERROR
           raise HTTPException(status_code=401,detail="No estas autorizado")
        return user
    
    def InfoUser(self, user: S.User_DB, db: Session) -> pd.DataFrame:
        if not self.Repo.readUs(db, user.email):
            raise HTTPException(status_code =404,detail="El usuario no existe")
        
        Consultas = self.Repo.readCons(db, user.email)
        return Consultas
    
    def UpdateUser(self, user: S.User_DB, new_data: S.User_DB, db: Session) -> HTTPException | None:
        if not self.Repo.readUs(db, user.email):
            raise HTTPException(status_code =404,detail="El usuario no existe")
        
        self.Repo.updateUs(db, user.email, new_data)
        return None
    def DeleteUser(self, user: S.User_DB, db: Session) -> HTTPException | None:
        if not self.Repo.readUs(db, user.email):
            raise HTTPException(status_code =404,detail="El usuario no existe")
        
        self.Repo.deleteUs(db, user.email)
        return None  