from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.database import Base


class Email(Base):

    __tablename__ = "emails"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=True
    )

    sender = Column(
        String(255)
    )

    recipient = Column(
        String(255)
    )

    subject = Column(
        String(500)
    )

    body = Column(
        Text
    )

    received_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )