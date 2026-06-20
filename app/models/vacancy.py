from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base
from datetime import datetime
class Vacancy(Base):
    __tablename__="vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    company:Mapped[str]
    description:Mapped[str]
    salary:Mapped[float]
    city:Mapped[str]
    type:Mapped[str]
    experience_years:Mapped[int]
    url:Mapped[str]=mapped_column(unique=True)
    source:Mapped[str]
    created_at:Mapped[datetime]
    parsed_at:Mapped[datetime]