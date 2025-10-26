from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .routers import api_router

app = FastAPI(title="PVZ Service", version="1.0.0")
app.include_router(api_router)
add_pagination(app)
