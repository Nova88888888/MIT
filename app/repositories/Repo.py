import app.repositories.TableModels as TM
from sqlalchemy.orm import Session
from app.schemes import Schemas as S
import pandas as pd
#Hashear contraseñas
class Repositorio:
    def __init__(self):
        pass

    def createUs(self, user: S.User_DB, db: Session, UsModel: TM.UserModel = TM.UserModel()) -> None:
        nuevo_usuario = TM.UserModel(name=user.name, password=user.password, email=user.email)
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

    def createCons(self, user: S.User_DB, db:Session, horario, CoModel: TM.ConsultasModel = TM.ConsultasModel()) -> None:
        nuevo_cons = TM.ConsultasModel(horario= horario, usuario= user.name)
        db.add(nuevo_cons)
        db.commit()
        db.refresh(nuevo_cons)

    def readUs(self, db:Session, email: str) -> S.User_DB | None:
           resp = db.get(TM.UserModel, email)
           if not resp:
            return resp
           else:
            Resp = S.User_DB.model_validate(resp)
            return Resp

    def readCons(self, db:Session, user: str,id: int = -1) -> S.Consulta | None:
        resp = db.query(TM.ConsultasModel).where(TM.ConsultasModel.usuario==user)# El user es un email
        if not resp:
               return resp
        if id == -1:
           resp =  [S.Consulta.model_validate(consulta) for consulta in resp]
           return resp
        else:
            resp = db.query(TM.ConsultasModel).where(TM.ConsultasModel.usuario==user, TM.ConsultasModel.id==id).first()
            if not resp:
                  return resp
            resp = S.Consulta.model_validate(resp)
            return resp
    def updateUs(self, db:Session, email:str, new_data: S.User_DB) -> None:
        user = db.get(TM.UserModel, email)
        if user:
            user.name = new_data.name
            user.password = new_data.password
            db.commit()
            db.refresh(user)
    def updateCons(self, db:Session, id:int, new_data: S.Consulta) -> None:
        cons = db.get(TM.ConsultasModel, id)
        if cons:
            cons.horario = new_data.horario
            db.commit()
            db.refresh(cons) 
    def deleteUs(self, db:Session, email:str) -> None:
        user = db.get(TM.UserModel, email)
        if user:
            db.delete(user)
            db.commit()
    def deleteCons(self, db:Session, id:str) -> None:
        cons = db.get(TM.ConsultasModel, id)
        if cons:
            db.delete(cons)
            db.commit()