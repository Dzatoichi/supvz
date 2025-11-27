from fastapi import FastAPI

from .routers import api_router
from .utils.exceptions import setup_exception_handlers
from .utils.middleware import LoggingMiddleware

app = FastAPI()
setup_exception_handlers(app)


app.add_middleware(LoggingMiddleware)
app.include_router(api_router)
