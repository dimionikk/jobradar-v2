import httpx
from datetime import datetime

REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"
WANTED_CATEGORIES = {
    "Software Development",
    "Devops",
    "Data and Analytics",
    "Quality Assurance",
    "Artificial Intelligence",
}


async def parse_remotive() -> list[dict]:
    vacancies = []

    async with httpx.AsyncClient() as client:
        response = await client.get(REMOTIVE_API_URL)
        response.raise_for_status()

        data = response.json()
        jobs = data.get("jobs", [])

        for job in jobs:
            category = job.get("category")
            if category not in WANTED_CATEGORIES:
                continue

            url = job.get("url")
            name = job.get("title")

            if not url or not name:
                continue

            published_at = None
            pub_date_text = job.get("publication_date")
            if pub_date_text:
                published_at = datetime.fromisoformat(pub_date_text)

            vacancies.append({
                "name": name,
                "url": url,
                "company": job.get("company_name"),
                "city": job.get("candidate_required_location"),
                "type": category,
                "salary": None,
                "description": job.get("description"),
                "published_at": published_at,
                "source": "remotive.com",
            })

    return vacancies