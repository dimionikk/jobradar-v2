from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    stack:Mapped[str | None] = mapped_column(nullable=True)
    experience_years:Mapped[int | None] = mapped_column(nullable=True)
    salary_expectation:Mapped[int | None] = mapped_column(nullable=True)
    city:Mapped[str | None] = mapped_column(nullable=True)
    work_type:Mapped[str | None] = mapped_column(nullable=True)
    bio:Mapped[str | None] = mapped_column(nullable=True)
    resume_text:Mapped[str | None] = mapped_column(nullable=True)