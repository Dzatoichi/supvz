# src/main.py
from fastapi import FastAPI
from .routers import api_router

app = FastAPI(
    title="My Auth Service",
)

app.include_router(api_router)
