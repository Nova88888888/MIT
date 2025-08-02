import sys
sys.path.append(".")

from fastapi import FastAPI
from app.controllers.routes import router
import uvicorn

App = FastAPI()
App.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app="app.main:App", reload=True)
    #http://127.0.0.1:8000/index