from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    stack:Mapped[str]
    experience_years:Mapped[int]
    salary_expectation:Mapped[int]
    city:Mapped[str]
    work_type:Mapped[str]
    bio:Mapped[str]