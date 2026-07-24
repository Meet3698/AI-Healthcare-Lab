from pydantic import BaseModel
from typing import Optional


class PatientCreate(BaseModel):

    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    medical_condition: Optional[str] = None


class PatientResponse(PatientCreate):

    id: int

    class Config:
        from_attributes = True