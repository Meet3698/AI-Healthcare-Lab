from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MedicalRecordCreate(BaseModel):

    patient_id: int
    doctor_id: Optional[int] = None
    diagnosis: Optional[str] = None
    notes: Optional[str] = None


class MedicalRecordResponse(MedicalRecordCreate):

    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True