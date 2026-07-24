from sqlalchemy.orm import Session

from app.services.ai_client import (

    client,

    model

)

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


    prompt = f"""

You are the Appointment Agent.

You are responsible only for appointments.

Patient appointments:

{appointments}

User request:

{user_message}

Answer using the available appointment information.

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
