from pydantic import BaseModel
from enum import Enum

class ApplicationStatus(str, Enum):
    applied = "applied"
    interview = "interview"
    rejected = "rejected"
    offer = "offer"


class ApplicationCreate(BaseModel):
    vacancy_id: int
    note: str

class ApplicationUpdate(BaseModel):
    status: ApplicationStatus