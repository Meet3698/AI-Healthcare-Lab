from sqlalchemy.orm import Session

from app.models.prescription import Prescription


def get_patient_prescriptions(
    patient_id: int,
    db: Session
):

    prescriptions = (
        db.query(Prescription)
        .filter(
            Prescription.patient_id == patient_id
        )
        .all()
    )

    return [
        {
            "id": prescription.id,
            "patient_id": prescription.patient_id,
            "doctor_id": prescription.doctor_id,
            "medicine": prescription.medicine,
            "dosage": prescription.dosage,
            "instructions": prescription.instructions,
            "created_at": (
                prescription.created_at.isoformat()
                if prescription.created_at
                else None
            )
        }
        for prescription in prescriptions
    ]