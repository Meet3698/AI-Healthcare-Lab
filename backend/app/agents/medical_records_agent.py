from sqlalchemy.orm import Session

from app.tools.medical_records_tool import (
    get_patient_records
)


def run_medical_records_agent(
    user_message: str,
    patient_id: int,
    db: Session
):

    records = get_patient_records(
        patient_id=patient_id,
        db=db
    )

    return {
        "agent": "medical_records_agent",
        "user_message": user_message,
        "records": records
    }