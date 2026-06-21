from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base
from sqlalchemy import ForeignKey,func
from datetime import datetime
class SavedVacancy(Base):
    __tablename__="saved_vacancies"
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
    vacancy_id:Mapped[int]=mapped_column(ForeignKey("vacancies.id"))
    saved_at: Mapped[datetime] = mapped_column(server_default=func.now())