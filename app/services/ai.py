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

async def generate_cover_letter(resume_text: str, vacancy_description: str) -> str:
    prompt = f"""Ти — асистент з написання супровідних листів (cover letter). На основі резюме кандидата та опису вакансії напиши короткий, персоналізований лист-відгук українською мовою.

Резюме кандидата:
{resume_text}

Опис вакансії:
{vacancy_description}

Вимоги до листа:
- 3-4 абзаци, без зайвої "води"
- Звернення на початку ("Шановний роботодавцю" або схоже, без конкретного імені)
- Підкресли саме ті навички з резюме, які реально релевантні цій вакансії
- Завершення з закликом до подальшої комунікації
- Пиши від першої особи, як ніби це сам кандидат

Не додавай жодних пояснень чи коментарів — лише сам текст листа."""

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text
