from fastapi import FastAPI

from source.api.server.routes import router as server_router
from source.api.service.routes import router as service_router
from source.api.auth import router as auth_router


def include_routers(app: FastAPI):
    """
    Функция для подключения всех роутеров к приложению FastAPI.
    """
    app.include_router(service_router)
    app.include_router(server_router)
    app.include_router(auth_router)


