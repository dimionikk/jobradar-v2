from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import database
from app.core.dependencies import get_current_user
from app.models import application as application_model
from app.models import user as user_model
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from app.models import vacancy as vacancy_model

router = APIRouter(prefix="/applications", tags=["applications"])

@router.get("/")
async def get_applications(
    current_user: user_model.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(application_model.Application).where(
            application_model.Application.user_id == current_user.id
        )
    )
    applications = result.scalars().all()
    return applications

@router.get("/{application_id}")
async def get_application(
    application_id: int,
    current_user: user_model.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(application_model.Application).where(
            application_model.Application.id == application_id,
            application_model.Application.user_id == current_user.id
        )
    )
    found_application = result.scalar_one_or_none()

    if found_application is None:
        raise HTTPException(status_code=404, detail="Заявка не знайдена")

    return found_application

@router.post("/")
async def create_application(
    data: ApplicationCreate,
    current_user: user_model.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(vacancy_model.Vacancy).where(vacancy_model.Vacancy.id == data.vacancy_id)
    )
    existing_vacancy = result.scalar_one_or_none()

    if existing_vacancy is None:
        raise HTTPException(status_code=404, detail="Вакансія не знайдена")

    new_application = application_model.Application(
        user_id=current_user.id,
        vacancy_id=data.vacancy_id,
        note=data.note,
        status="applied"
    )
    db.add(new_application)
    await db.commit()

    return new_application

@router.patch("/{application_id}")
async def update_application_status(
    application_id: int,
    data: ApplicationUpdate,
    current_user: user_model.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(application_model.Application).where(
            application_model.Application.id == application_id,
            application_model.Application.user_id == current_user.id
        )
    )
    found_application = result.scalar_one_or_none()

    if found_application is None:
        raise HTTPException(status_code=404, detail="Заявка не знайдена")

    found_application.status = data.status
    await db.commit()

    return found_application

@router.delete("/{application_id}")
async def delete_application(
    application_id: int,
    current_user: user_model.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(application_model.Application).where(
            application_model.Application.id == application_id,
            application_model.Application.user_id == current_user.id
        )
    )
    found_application = result.scalar_one_or_none()

    if found_application is None:
        raise HTTPException(status_code=404, detail="Заявка не знайдена")

    await db.delete(found_application)
    await db.commit()

    return {"status": "deleted"}