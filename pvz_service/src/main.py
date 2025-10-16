from fastapi import FastAPI

from .routers import api_router

app = FastAPI(title="PVZ Service", version="1.0.0")
app.include_router(api_router)
