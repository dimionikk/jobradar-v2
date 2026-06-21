from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    vacancy_id: int
    note: str