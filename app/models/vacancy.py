from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import datetime


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    company: Mapped[str]
    description: Mapped[str]
    salary: Mapped[float | None] = mapped_column(nullable=True)
    city: Mapped[str | None] = mapped_column(nullable=True)
    type: Mapped[str | None] = mapped_column(nullable=True)
    experience_years: Mapped[int | None] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(unique=True)
    source: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    published_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime]
    parsed_at: Mapped[datetime]