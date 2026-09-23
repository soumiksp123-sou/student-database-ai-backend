
from pydantic import BaseModel, EmailStr, ConfigDict


class StudentBase(BaseModel):
    name: str
    age: int
    gender: str
    department: str
    email: EmailStr
    phone: str
    gpa: float


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    gender: str | None = None
    department: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    gpa: float | None = None


class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
