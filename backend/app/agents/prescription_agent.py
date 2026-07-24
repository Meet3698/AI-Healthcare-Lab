from sqlalchemy.orm import Session

from app.tools.prescriptions_tool import (
    get_prescriptions_for_patient,
)


def run_prescription_agent(
    user_message: str,
    patient_id: int,
    db: Session,
):
    prescriptions = get_prescriptions_for_patient(
        patient_id=patient_id,
        db=db,
    )

    if not prescriptions:
        return {
            "agent": "prescriptions_agent",
            "message": "No prescriptions found for this patient.",
            "data": [],
        }

    return {
        "agent": "prescriptions_agent",
        "message": "Prescription records retrieved successfully.",
        "data": prescriptions,
    }