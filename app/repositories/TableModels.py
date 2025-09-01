from sqlalchemy import String, Integer, Column, ForeignKey
from app.repositories.DataBase import DBase
from sqlalchemy.orm import relationship

class UserModel(DBase):
    __tablename__ = "UserModel"

    name = Column(String, unique= True)
    password = Column(String)
    email = Column(String, primary_key=True,unique=True)
    
    us = relationship("ConsultasModel",back_populates="cons",uselist=False)
class ConsultasModel(DBase):
    __tablename__ = "ConsultasModel"

    id = Column(Integer, unique= True, index=True, primary_key=True)
    horario = Column(String)  #Debe ser de valor Time
    usuario = Column(String, ForeignKey("UserModel.email"))
    usuario = Column(String, ForeignKey("UserModel.email"))
    
    cons = relationship("UserModel",back_populates="us")
