from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.database import Base


class LabReport(Base):

    __tablename__ = "lab_reports"

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

    file_name = Column(
        String(255)
    )

    file_path = Column(
        String(500)
    )

    extracted_text = Column(
        Text
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )