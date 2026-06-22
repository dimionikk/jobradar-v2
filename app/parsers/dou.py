import re
import httpx
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

DOU_RSS_URL = "https://jobs.dou.ua/vacancies/feeds/"

SALARY_PATTERN = re.compile(r"^\$(\d+)(?:[-–](\d+))?$")


def parse_salary(text: str) -> float | None:
    match = SALARY_PATTERN.match(text)
    if not match:
        return None

    low = float(match.group(1))
    high = float(match.group(2)) if match.group(2) else low
    return (low + high) / 2


def parse_title(title: str) -> tuple[str, str, str | None, float | None]:
    name_part, rest = title.split(" в ", maxsplit=1)

    if "," not in rest:
        return name_part, rest, None, None

    company, remainder = rest.split(", ", maxsplit=1)

    if "," in remainder:
        first_part, after_first = remainder.split(", ", maxsplit=1)
    else:
        first_part, after_first = remainder, None

    salary = parse_salary(first_part)

    if salary is not None:
        city = after_first
    else:
        city = remainder

    return name_part, company, city, salary


async def parse_dou() -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(DOU_RSS_URL)
        response.raise_for_status()

    root = ET.fromstring(response.text)
    items = root.findall(".//item")

    vacancies = []
    for item in items:
        title_text = item.find("title").text
        link = item.find("link").text
        description = item.find("description").text
        pub_date_text = item.find("pubDate").text

        if not title_text or not link:
            continue

        name, company, city, salary = parse_title(title_text)

        vacancies.append({
            "name": name,
            "url": link,
            "company": company,
            "city": city,
            "salary": salary,
            "description": description,
            "published_at": parsedate_to_datetime(pub_date_text).replace(tzinfo=None),
            "source": "dou.ua",
        })

    return vacancies