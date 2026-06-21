from fastapi import FastAPI
from app.routers import auth, vacancies

app = FastAPI(title="JobRadar")

app.include_router(auth.router)
app.include_router(vacancies.router)