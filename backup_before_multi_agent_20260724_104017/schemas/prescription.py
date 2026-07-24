from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PrescriptionCreate(BaseModel):

    patient_id: int
    doctor_id: Optional[int] = None
    medicine: str
    dosage: Optional[str] = None
    instructions: Optional[str] = None


class PrescriptionResponse(PrescriptionCreate):

    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True