from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.patient import Patient
from app.models.prescription import Prescription
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionResponse
)


router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)


@router.post(
    "/",
    response_model=PrescriptionResponse
)
def create_prescription(
    prescription_data: PrescriptionCreate,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(
            Patient.id == prescription_data.patient_id
        )
        .first()
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    new_prescription = Prescription(
        patient_id=prescription_data.patient_id,
        doctor_id=prescription_data.doctor_id,
        medicine=prescription_data.medicine,
        dosage=prescription_data.dosage,
        instructions=prescription_data.instructions
    )

    db.add(new_prescription)

    db.commit()

    db.refresh(new_prescription)

    return new_prescription

@router.get(
    "/",
    response_model=list[PrescriptionResponse]
)
def get_prescriptions(
    db: Session = Depends(get_db)
):

    return db.query(Prescription).all()

@router.get(
    "/{prescription_id}",
    response_model=PrescriptionResponse
)
def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db)
):

    prescription = (
        db.query(Prescription)
        .filter(
            Prescription.id == prescription_id
        )
        .first()
    )

    if not prescription:

        raise HTTPException(
            status_code=404,
            detail="Prescription not found"
        )

    return prescription