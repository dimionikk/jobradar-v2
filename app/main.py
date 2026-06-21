from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="JobRadar")

app.include_router(auth.router)