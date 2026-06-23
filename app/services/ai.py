from anthropic import AsyncAnthropic
from app.core.config import settings

client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)


async def analyze_match(resume_text: str, vacancy_description: str) -> str:
    prompt = f"""Ти — асистент з підбору персоналу. Порівняй резюме кандидата з описом вакансії.

Резюме кандидата:
{resume_text}

Опис вакансії:
{vacancy_description}

Дай відповідь у такому форматі:
1. Відсоток відповідності (0-100%)
2. Короткий висновок (2-3 речення) — чому саме такий відсоток, які ключові навички співпадають, чого не вистачає.

Відповідай українською мовою."""

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text