from sqlalchemy.orm import Session

from app.models.medical_record import MedicalRecord


def get_patient_records(
    patient_id: int,
    db: Session
):

    records = (
        db.query(MedicalRecord)
        .filter(
            MedicalRecord.patient_id == patient_id
        )
        .all()
    )

    return [
        {
            "id": record.id,
            "patient_id": record.patient_id,
            "diagnosis": record.diagnosis,
            "notes": record.notes,
            "created_at": (
                record.created_at.isoformat()
                if record.created_at
                else None
            )
        }
        for record in records
    ]