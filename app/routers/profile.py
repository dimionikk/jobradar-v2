from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import database
from app.core.dependencies import get_current_user
from app.models import user as user_model
from app.schemas.user import ProfileUpdate,ProfileOut

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/",response_model=ProfileOut)
async def get_profile(
    current_user: user_model.User = Depends(get_current_user)
):
    return current_user


@router.patch("/",response_model=ProfileOut)
async def update_profile(
    data: ProfileUpdate,
    current_user: user_model.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    if data.stack is not None:
        current_user.stack = data.stack

    if data.experience_years is not None:
        current_user.experience_years = data.experience_years

    if data.salary_expectation is not None:
        current_user.salary_expectation = data.salary_expectation

    if data.city is not None:
        current_user.city = data.city

    if data.work_type is not None:
        current_user.work_type = data.work_type

    if data.bio is not None:
        current_user.bio = data.bio

    if data.resume_text is not None:
        current_user.resume_text = data.resume_text

    await db.commit()

    return current_user