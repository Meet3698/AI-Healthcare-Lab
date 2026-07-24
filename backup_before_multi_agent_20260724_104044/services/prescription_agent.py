from sqlalchemy.orm import Session

from app.services.ai_client import (

    client,

    model

)

from app.tools.prescriptions_tool import (

    get_patient_prescriptions

)


def run_prescription_agent(

    user_message: str,

    patient_id: int,

    db: Session

):

    prescriptions = get_patient_prescriptions(

        patient_id=patient_id,

        db=db

    )


    prompt = f"""

You are the Prescription Agent.

You are responsible only for prescriptions and medicines.

Patient prescriptions:

{prescriptions}

User request:

{user_message}

Answer using the available prescription information.

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
