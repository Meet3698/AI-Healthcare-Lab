from sqlalchemy.orm import Session

from app.models.appointment import Appointment


def get_patient_appointments(
    patient_id: int,
    db: Session
):

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.patient_id == patient_id
        )
        .all()
    )

    return [
        {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "appointment_time": (
                appointment.appointment_time.isoformat()
                if appointment.appointment_time
                else None
            ),
            "status": appointment.status
        }
        for appointment in appointments
    ]