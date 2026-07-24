from sqlalchemy.orm import Session

from app.agents.medical_records_agent import (
    run_medical_records_agent
)

from app.agents.prescription_agent import (
    run_prescription_agent
)

from app.agents.appointment_agent import (
    run_appointment_agent
)


def run_supervisor_agent(
    user_message: str,
    patient_id: int,
    db: Session
):

    message = user_message.lower()

    if (
        "medical record" in message
        or "medical history" in message
        or "diagnosis" in message
    ):

        return run_medical_records_agent(
            user_message=user_message,
            patient_id=patient_id,
            db=db
        )


    if (
        "prescription" in message
        or "medicine" in message
        or "medication" in message
    ):

        return run_prescription_agent(
            user_message=user_message,
            patient_id=patient_id,
            db=db
        )


    if (
        "appointment" in message
        or "doctor" in message
        or "schedule" in message
    ):

        return run_appointment_agent(
            user_message=user_message,
            patient_id=patient_id,
            db=db
        )


    return {

        "agent": "supervisor_agent",

        "message": (
            "I could not determine which "
            "specialized healthcare agent "
            "should handle this request."
        )

    }