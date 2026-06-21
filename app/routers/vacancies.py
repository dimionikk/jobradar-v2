from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import database
from app.models import vacancy as vacancy_model

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

@router.get("/")
async def get_vacancies(
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(database.get_db)
):
    offset = (page - 1) * limit
    result = await db.execute(select(vacancy_model.Vacancy).offset(offset).limit(limit))
    vacancies = result.scalars().all()
    return vacancies

@router.get("/{vacancy_id}")
async def get_vacancy(vacancy_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(vacancy_model.Vacancy).where(vacancy_model.Vacancy.id == vacancy_id))
    found_vacancy = result.scalar_one_or_none()

    if found_vacancy is None:
        raise HTTPException(status_code=404, detail="Вакансія не знайдена")

    return found_vacancy