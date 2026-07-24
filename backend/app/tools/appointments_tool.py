from sqlalchemy.orm import Session

from app.models.appointment import Appointment


def get_patient_appointments(
    patient_id: int,
    db: Session,
):
    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.patient_id == patient_id
        )
        .all()
    )

    results = []

    for appointment in appointments:
        appointment_data = {}

        for column in Appointment.__table__.columns:
            value = getattr(
                appointment,
                column.name,
                None,
            )

            if hasattr(value, "isoformat"):
                value = value.isoformat()

            appointment_data[column.name] = value

        results.append(appointment_data)

    return results