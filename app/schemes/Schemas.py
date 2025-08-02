from pydantic import BaseModel
from enum import Enum

class User(BaseModel):
    name: str
    password: str
    email: str

class Consulta(BaseModel):
    id: int
    horario: str # Time
    user: str
    
class ConfirmResponse(str, Enum):
    Positivo = "Funciono Correctamente"
    Negativo = "Ha hecho algo mal"
    ErrorServ = "Error del Servidor"
