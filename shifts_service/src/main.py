from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .routers import api_router
from .utils.exception_handler import setup_exception_handlers

app = FastAPI()
setup_exception_handlers(app)

app.include_router(api_router)
add_pagination(app)
