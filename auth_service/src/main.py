from fastapi import FastAPI

from .routers import api_router
from .utils.exceptions import setup_exception_handlers

app = FastAPI()
setup_exception_handlers(app)

app.include_router(api_router)
