from sqlalchemy.orm import Session

from app.tools.medical_records_tool import (
    get_patient_records
)

from app.services.ai_service import ask_ai


def run_agent(
    user_message: str,
    patient_id: int,
    db: Session
):

    message = user_message.lower()

    if (
        "medical record" in message
        or "medical records" in message
        or "diagnosis" in message
    ):

        records = get_patient_records(
            patient_id=patient_id,
            db=db
        )

        prompt = f"""
You are a healthcare assistant.

The following medical records belong to
the patient:

{records}

User question:

{user_message}

Answer using only the provided records.
If the records do not contain the answer,
say that the information is not available.
"""

        return ask_ai(prompt)

    return ask_ai(user_message)