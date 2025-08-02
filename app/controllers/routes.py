<<<<<<< HEAD
from fastapi import FastAPI, Request, APIRouter, status
from fastapi.staticfiles import StaticFiles
=======
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import FastAPI, Request, APIRouter, status, Depends
>>>>>>> 7b0056a299c168c7a34419bbec39d1b6e969d30e
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from repositories.DataBase import Get_db
from schemes import Schemas as S
from services.Email import Email_Serv

router = APIRouter(responses={status.HTTP_404_NOT_FOUND: {"message":"No Encontrado"}}) 
Service = Email_Serv()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="portal-paciente")
# Carga las plantillas desde la carpeta "templates"
templates = Jinja2Templates(directory="app/controllers/templates")

<<<<<<< HEAD
router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/")
async def Indexium():
    return {"Heero":"hello"}

@router.get("/index", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
=======
@router.get("/index", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
#token: str = Depends(oauth2_bearer)
@router.post("/portal-paciente")
def LogIn(form: OAuth2PasswordRequestForm = Depends()): 
    #user: S.User = {"name":form.username, "password":form.password, "email": form.e-mail} R
    message = Service.LogIn(form)
    return message

@router.post("/registr/{user}")
def Registr(user: S.User):
    message = Service.Registro(user, db: Session = Depends(Get_DB))
    return {"message":message}
>>>>>>> 7b0056a299c168c7a34419bbec39d1b6e969d30e
