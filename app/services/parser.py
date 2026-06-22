from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import vacancy as vacancy_model


async def save_vacancies(db: AsyncSession, parsed_vacancies: list[dict], source: str) -> None:
    seen_urls = []

    for item in parsed_vacancies:
        seen_urls.append(item["url"])

        result = await db.execute(
            select(vacancy_model.Vacancy).where(vacancy_model.Vacancy.url == item["url"])
        )
        existing_vacancy = result.scalar_one_or_none()

        if existing_vacancy is None:
            new_vacancy = vacancy_model.Vacancy(
                name=item["name"],
                company=item["company"],
                description=item["description"],
                salary=item.get("salary"),
                city=item["city"],
                type=item.get("type"),
                experience_years=item.get("experience_years"),
                url=item["url"],
                source=source,
                is_active=True,
                created_at=datetime.now(),
                parsed_at=datetime.now(),
            )
            db.add(new_vacancy)
        else:
            existing_vacancy.parsed_at = datetime.now()
            existing_vacancy.is_active = True

    result = await db.execute(
        select(vacancy_model.Vacancy).where(
            vacancy_model.Vacancy.source == source,
            vacancy_model.Vacancy.url.notin_(seen_urls)
        )
    )
    outdated_vacancies = result.scalars().all()

    for vacancy in outdated_vacancies:
        vacancy.is_active = False

    await db.commit()