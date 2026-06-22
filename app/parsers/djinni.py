import httpx
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

DJINNI_RSS_URL = "https://djinni.co/jobs/rss/"


async def parse_djinni() -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(DJINNI_RSS_URL)
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

        category_tags = item.findall("category")
        category = None
        for tag in category_tags:
            if tag.text:
                category = tag.text
                break

        vacancies.append({
            "name": title_text,
            "url": link,
            "company": None,
            "city": None,
            "type": category,
            "description": description,
            "published_at": parsedate_to_datetime(pub_date_text).replace(tzinfo=None),
            "source": "djinni.co",
        })

    return vacancies