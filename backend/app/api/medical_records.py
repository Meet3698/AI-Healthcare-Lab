from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.medical_record import MedicalRecord
from app.models.patient import Patient
from app.schemas.medical_record import (
    MedicalRecordCreate,
    MedicalRecordResponse
)


router = APIRouter(
    prefix="/records",
    tags=["Medical Records"]
)


@router.post(
    "/",
    response_model=MedicalRecordResponse
)
def create_medical_record(
    record_data: MedicalRecordCreate,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(Patient.id == record_data.patient_id)
        .first()
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    new_record = MedicalRecord(
        patient_id=record_data.patient_id,
        doctor_id=record_data.doctor_id,
        diagnosis=record_data.diagnosis,
        notes=record_data.notes
    )

    db.add(new_record)

    db.commit()

    db.refresh(new_record)

    return new_record

@router.get(
    "/",
    response_model=list[MedicalRecordResponse]
)
def get_medical_records(
    db: Session = Depends(get_db)
):

    return db.query(MedicalRecord).all()

@router.get(
    "/{record_id}",
    response_model=MedicalRecordResponse
)
def get_medical_record(
    record_id: int,
    db: Session = Depends(get_db)
):

    record = (
        db.query(MedicalRecord)
        .filter(MedicalRecord.id == record_id)
        .first()
    )

    if not record:

        raise HTTPException(
            status_code=404,
            detail="Medical record not found"
        )

    return record