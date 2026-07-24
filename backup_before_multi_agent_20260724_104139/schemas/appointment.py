from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AppointmentCreate(BaseModel):

    patient_id: int
    doctor_id: Optional[int] = None
    appointment_time: datetime
    status: Optional[str] = "scheduled"


class AppointmentResponse(AppointmentCreate):

    id: int

    class Config:
        from_attributes = True