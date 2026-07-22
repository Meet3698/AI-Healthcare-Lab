from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientResponse
from app.models.medical_record import MedicalRecord
from app.schemas.medical_record import MedicalRecordResponse
from app.models.prescription import Prescription
from app.schemas.prescription import PrescriptionResponse


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.get(
    "/",
    response_model=list[PatientResponse]
)
def get_patients(
    db: Session = Depends(get_db)
):

    return db.query(Patient).all()


@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient

@router.put(
    "/{patient_id}",
    response_model=PatientResponse
)
def update_patient(
    patient_id: int,
    patient_data: PatientCreate,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    patient.name = patient_data.name
    patient.age = patient_data.age
    patient.gender = patient_data.gender
    patient.email = patient_data.email
    patient.phone = patient_data.phone
    patient.medical_condition = patient_data.medical_condition

    db.commit()

    db.refresh(patient)

    return patient

@router.delete(
    "/{patient_id}"
)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)

    db.commit()

    return {
        "message": "Patient deleted successfully"
    }

@router.post(
    "/",
    response_model=PatientResponse
)
def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db)
):

    new_patient = Patient(
        name=patient_data.name,
        age=patient_data.age,
        gender=patient_data.gender,
        email=patient_data.email,
        phone=patient_data.phone,
        medical_condition=patient_data.medical_condition
    )

    db.add(new_patient)

    db.commit()

    db.refresh(new_patient)

    return new_patient

@router.get(
    "/{patient_id}/records",
    response_model=list[MedicalRecordResponse]
)
def get_patient_records(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return (
        db.query(MedicalRecord)
        .filter(MedicalRecord.patient_id == patient_id)
        .all()
    )

@router.get(
    "/{patient_id}/prescriptions",
    response_model=list[PrescriptionResponse]
)
def get_patient_prescriptions(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return (
        db.query(Prescription)
        .filter(
            Prescription.patient_id == patient_id
        )
        .all()
    )