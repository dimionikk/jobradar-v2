from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.database import AsyncSessionLocal
from app.parsers.dou import parse_dou
from app.parsers.djinni import parse_djinni
from app.parsers.workua import parse_workua
from app.parsers.remotive import parse_remotive
from app.services.parser import save_vacancies

scheduler = AsyncIOScheduler()


async def run_parser_job(parser_func, source: str):
    parsed = await parser_func()
    async with AsyncSessionLocal() as db:
        await save_vacancies(db, parsed, source=source)


def start_scheduler():
    scheduler.add_job(run_parser_job, "interval", hours=3, args=[parse_dou, "dou.ua"])
    scheduler.add_job(run_parser_job, "interval", hours=3, args=[parse_djinni, "djinni.co"])
    scheduler.add_job(run_parser_job, "interval", hours=3, args=[parse_workua, "work.ua"])
    scheduler.add_job(run_parser_job, "interval", hours=6, args=[parse_remotive, "remotive.com"])

    scheduler.start()