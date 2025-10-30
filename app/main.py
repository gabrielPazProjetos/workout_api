from fastapi import FastAPI
from app.routers import atleta
from fastapi_pagination import add_pagination

app = FastAPI(title="Workout API")

app.include_router(atleta.router, prefix="/atletas", tags=["Atletas"])

add_pagination(app)
