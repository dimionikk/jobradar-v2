from fastapi import FastAPI
from app.routers import auth, vacancies, saved, applications

app = FastAPI(title="JobRadar")

app.include_router(auth.router)
app.include_router(vacancies.router)
app.include_router(saved.router)
app.include_router(applications.router)