from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import auth, vacancies, saved, applications
from app.core.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield


app = FastAPI(title="JobRadar", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(vacancies.router)
app.include_router(saved.router)
app.include_router(applications.router)