from sqlalchemy.orm import Session

from app.models.prescription import Prescription


def get_prescriptions_for_patient(
    patient_id: int,
    db: Session,
):
    prescriptions = (
        db.query(Prescription)
        .filter(
            Prescription.patient_id == patient_id
        )
        .all()
    )

    results = []

    for prescription in prescriptions:
        prescription_data = {}

        for column in Prescription.__table__.columns:
            value = getattr(
                prescription,
                column.name,
                None,
            )

            if hasattr(value, "isoformat"):
                value = value.isoformat()

            prescription_data[column.name] = value

        results.append(prescription_data)

    return results