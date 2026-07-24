from sqlalchemy.orm import Session

from app.tools.appointments_tool import (
    get_patient_appointments
)


def run_appointment_agent(
    user_message: str,
    patient_id: int,
    db: Session
):

    appointments = get_patient_appointments(
        patient_id=patient_id,
        db=db
    )

    return {
        "agent": "appointment_agent",
        "user_message": user_message,
        "appointments": appointments
    }