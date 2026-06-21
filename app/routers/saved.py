from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import database
from app.core.dependencies import get_current_user
from app.models import saved_vacancy as saved_vacancy_model
from app.models import user as user_model

router = APIRouter(prefix="/saved", tags=["saved"])


@router.get("/")
async def get_saved_vacancies(
    current_user: user_model.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(saved_vacancy_model.SavedVacancy).where(
            saved_vacancy_model.SavedVacancy.user_id == current_user.id
        )
    )
    saved = result.scalars().all()
    return saved


@router.post("/{vacancy_id}")
async def save_vacancy(
    vacancy_id: int,
    current_user: user_model.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(saved_vacancy_model.SavedVacancy).where(
            saved_vacancy_model.SavedVacancy.user_id == current_user.id,
            saved_vacancy_model.SavedVacancy.vacancy_id == vacancy_id
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Вакансія вже збережена")

    new_saved = saved_vacancy_model.SavedVacancy(user_id=current_user.id, vacancy_id=vacancy_id)
    db.add(new_saved)
    await db.commit()

    return new_saved


@router.delete("/{vacancy_id}")
async def delete_saved_vacancy(
    vacancy_id: int,
    current_user: user_model.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(saved_vacancy_model.SavedVacancy).where(
            saved_vacancy_model.SavedVacancy.user_id == current_user.id,
            saved_vacancy_model.SavedVacancy.vacancy_id == vacancy_id
        )
    )
    existing = result.scalar_one_or_none()

    if existing is None:
        raise HTTPException(status_code=404, detail="Збережена вакансія не знайдена")

    await db.delete(existing)
    await db.commit()

    return {"status": "deleted"}