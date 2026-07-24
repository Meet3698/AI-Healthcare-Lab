from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database.database import Base


class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    doctor_id = Column(
        Integer,
        nullable=True
    )

    appointment_time = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        String(50),
        default="scheduled"
    )