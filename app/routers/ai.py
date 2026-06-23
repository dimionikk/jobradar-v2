from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import database
from app.core.dependencies import get_current_user
from app.models import user as user_model
from app.models import vacancy as vacancy_model
from app.services.ai import analyze_match

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/match/{vacancy_id}")
async def match_vacancy(
    vacancy_id: int,
    current_user: user_model.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    if not current_user.resume_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Спочатку заповни resume_text у профілі (PATCH /profile/)"
        )

    result = await db.execute(
        select(vacancy_model.Vacancy).where(vacancy_model.Vacancy.id == vacancy_id)
    )
    vacancy = result.scalar_one_or_none()

    if vacancy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансію не знайдено"
        )

    analysis = await analyze_match(current_user.resume_text, vacancy.description)

    return {
        "vacancy_id": vacancy.id,
        "vacancy_name": vacancy.name,
        "analysis": analysis,
    }