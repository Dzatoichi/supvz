from fastapi import FastAPI

from . import routes

app = FastAPI(title='Auth')

app.include_router(routes.auth_router)
