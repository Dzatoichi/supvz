from fastapi import FastAPI

from src.routers.employees_router import employees_router

app = FastAPI(title="PVZ Service", version="1.0.0")
app.include_router(employees_router)
