import httpx
from datetime import datetime
from bs4 import BeautifulSoup

WORKUA_BASE_URL = "https://www.work.ua/jobs-it/"
PAGES_TO_PARSE = 5

MONTHS_UA = {
    "січня": 1, "лютого": 2, "березня": 3, "квітня": 4,
    "травня": 5, "червня": 6, "липня": 7, "серпня": 8,
    "вересня": 9, "жовтня": 10, "листопада": 11, "грудня": 12,
}


def parse_workua_date(date_text: str) -> datetime | None:
    try:
        day_text, month_text, year_text = date_text.split()
        day = int(day_text)
        month = MONTHS_UA[month_text]
        year = int(year_text)
        return datetime(year, month, day)
    except (ValueError, KeyError):
        return None


async def parse_workua() -> list[dict]:
    vacancies = []

    async with httpx.AsyncClient() as client:
        for page in range(1, PAGES_TO_PARSE + 1):
            response = await client.get(WORKUA_BASE_URL, params={"page": page})
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select("div.job-link")

            for card in cards:
                title_tag = card.select_one("h2 a")
                company_tag = card.select_one("span.strong-600")
                description_tag = card.select_one("p.ellipsis")

                if not title_tag:
                    continue

                url = "https://www.work.ua" + title_tag["href"]
                name = title_tag.get_text(strip=True)

                title_attr = title_tag.get("title", "")
                published_at = None
                if ", вакансія від " in title_attr:
                    _, date_text = title_attr.split(", вакансія від ", maxsplit=1)
                    published_at = parse_workua_date(date_text)

                vacancies.append({
                    "name": name,
                    "url": url,
                    "company": company_tag.get_text(strip=True) if company_tag else None,
                    "city": None,
                    "description": description_tag.get_text(strip=True).replace("\xa0", " ").replace("\n", " ") if description_tag else None,
                    "published_at": published_at,
                    "source": "work.ua",
                })

    return vacancies