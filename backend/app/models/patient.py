from sqlalchemy import Column, Integer, String, Text

from app.database.database import Base


class Patient(Base):

    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    age = Column(
        Integer
    )

    gender = Column(
        String(20)
    )

    email = Column(
        String(150)
    )

    phone = Column(
        String(20)
    )

    medical_condition = Column(
        Text
    )