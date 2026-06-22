import httpx
from bs4 import BeautifulSoup

DOU_URL = "https://jobs.dou.ua/vacancies/"


async def parse_dou() -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(DOU_URL)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    vacancy_items = soup.select("li.l-vacancy")

    vacancies = []
    for item in vacancy_items:
        title_tag = item.select_one("a.vt")
        company_tag = item.select_one("a.company")
        city_tag = item.select_one("span.cities")
        description_tag = item.select_one("div.sh-info")

        if not title_tag or not company_tag:
            continue

        vacancies.append({
            "name": title_tag.get_text(strip=True),
            "url": title_tag["href"],
            "company": company_tag.get_text(strip=True),
            "city": city_tag.get_text(strip=True) if city_tag else None,
            "description": description_tag.get_text(strip=True).replace("\xa0", " ").replace("\n", " ") if description_tag else None,
            "source": "dou.ua",
        })

    return vacancies