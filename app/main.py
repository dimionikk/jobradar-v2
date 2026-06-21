from fastapi import FastAPI
from app.routers import auth, vacancies, saved

app = FastAPI(title="JobRadar")

app.include_router(auth.router)
app.include_router(vacancies.router)
app.include_router(saved.router)