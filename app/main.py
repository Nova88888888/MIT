import sys
sys.path.append(".")

import uvicorn
from fastapi import FastAPI
from app.controllers.routes import router
from app.repositories.DataBase import DBase, Engine

App = FastAPI()
App.include_router(router)
DBase.metadata.create_all(bind=Engine)

if __name__ == "__main__":
    uvicorn.run(app="app.main:App", reload=True)

"""def custom_openapi():
    if App.openapi_schema:
        return App.openapi_schema

    openapi_schema = get_openapi(
        title=App.title,
        version=App.version,
        description=App.description,
        routes=App.routes,
    )

    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply global security requirement
    openapi_schema["security"] = [{"BearerAuth": []}]

    App.openapi_schema = openapi_schema
    return App.openapi_schema

App.openapi = custom_openapi"""