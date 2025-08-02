import TableModels as TM
from sqlalchemy.orm import Session
from schemes import Schemas as S
import pandas as pd
#Hashear contraseñas
class Repositorio:
    def __init__(self):
        pass

    def createUs(self, user: S.User, db: Session, UsModel: TM.UserModel = TM.UserModel()) -> None:
        nuevo_producto = Usuario(nombre=user.name, password=user.password, email=user.email)
        db.add(nuevo_producto)
        db.commit()
        db.refresh(Usuario)

    def createCons(self, user: S.User, db:Session, CoModel: TM.ConsultasModel = TM.ConsultasModel(), horario) -> None:
        nuevo_producto = Consulta(horario= horario, usuario= user.name)
        db.add(nuevo_producto)
        db.commit()
        db.refresh(Consulta)

    def readUs(self, user: S.User | bool = False, db:Session) -> S.User | pd.DataFrame:
        if user != False:
           resp = db.query(TM.UserModel).filter_by(name=user.name).all()
           Resp = dict(resp)
           return Resp
        else: 
            resp = db.query(TM.UserModel).all()
            dfResp = pd.DataFrame(resp)
            return dfResp

    def readCons(self, cons: S.Consulta | bool = False, db:Session) -> S.Consulta | pd.DataFrame:
        if user != False:
           resp = db.query(TM.ConsultasModel).where(id==cons.id)
           resp = dict(resp)
           return resp
        else: 
            resp = db.query(TM.ConsultasModel).all()
            dfresp = pd.DataFrame(resp)
            return dfresp
        