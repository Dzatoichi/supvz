from fastapi import FastAPI

from .routers import api_router
from .utils.exceptions_handler import setup_exception_handlers

app = FastAPI(title="PVZ Service", version="1.0.0")
app.include_router(api_router)
setup_exception_handlers(app)
