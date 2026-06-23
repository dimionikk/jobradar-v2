from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProfileUpdate(BaseModel):
    stack: str | None = None
    experience_years: int | None = None
    salary_expectation: int | None = None
    city: str | None = None
    work_type: str | None = None
    bio: str | None = None
    resume_text: str | None = None

class ProfileOut(BaseModel):
    id: int
    email: str
    stack: str | None
    experience_years: int | None
    salary_expectation: int | None
    city: str | None
    work_type: str | None
    bio: str | None
    resume_text: str | None

    class Config:
        from_attributes = True