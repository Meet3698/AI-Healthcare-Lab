from sqlalchemy.orm import Session

from app.services.ai_client import (

    client,

    model

)

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


    prompt = f"""

You are the Medical Records Agent.

You are responsible only for medical records.

Patient medical records:

{records}

User request:

{user_message}

Answer using the available patient records.

"""


    response = client.chat.completions.create(

        model=model,

        messages=[

            {

                "role": "system",

                "content": prompt

            }

        ]

    )


    return response.choices[0].message.content
