from email_validator import validate_emailadress, EmailNotValidError
from smtplib import SMTP_SSL
from email import EmailMessage
from schemes import Schemas as S
from repositories.Repo import Repositorio
import pandas as pd
from fastapi import HTTPException

import os
from dotenv import load_dotenv
load_dotenv()
passwordE = os.getenv("password")

class Email_Serv(): 
    def __init__(self, email, password, Repo):
        email = "CentroMedicodeInvestigaciónyTratamientoyahoomail.com"
        __password = passwordE
        Repo = Repositorio()
    def Notificacion(self, user: S.User, message: str): #Envia una notificacion a un Usuario
        Notificacc = EmailMessage()
        Notificacc["Subject"] = "MIT"
        Notificacc["From"] = self.email
        Notificacc["Subject"] = user.email
        Notificacc.set_content = message
        with SMTP_SSL("smtp.gmail.com") as conn:
          conn.login(self.email, passwordE)
          conn.send_message(Notificacc)

    def ValEmail(self, email:str) -> bool:
          valid = validate_emailadress(email, check_deliverability=True)
          if valid == EmailNotValidError:
              raise False
          else:
              return True
        
    def Registro(self, user:S.User, db:Session) -> str:
        Users: pd.DataFrame = self.Repo.readUs(False, db)

        if user.name in Users.name:
            raise "Ese nombre ya estâ usado"
        email_val: bool = ValEmail(user.email)

        if not email_val:
            raise "Email no válido"
        if user.email in Users.email:
            raise "Ya tienes una cuenta con ese correo"

        """<Solicitud a DB>"""
        self.Repo.createUs(user, db)
        return "Se ha registrado correctamente"
    #[]
    def LogIn(self, user: S.User) :
      Users: pd.DataFrame = self.Repo.readUs(False, db)
      for p in range(len(Users.password)):
        if Users.password[p] != user.password:
            raise HTTPException(status_code=400, detail="Contraseña incorrecta")
        elif user.username != Users.name[p]:
            raise HTTPException(status_code=400, detail="Usuario Incorrecto")
        else:
           return {"access_token": user.username, "token_type": "bearer"}  #user.username debe ser un valor encriptado

