from sqlalchemy.orm import Session

from app.services.ai_client import (

    client,

    model

)

from app.services.medical_records_agent import (

    run_medical_records_agent

)

from app.services.prescription_agent import (

    run_prescription_agent

)

from app.services.appointment_agent import (

    run_appointment_agent

)


def run_supervisor_agent(

    user_message: str,

    patient_id: int,

    db: Session

):

    routing_prompt = f"""

You are the Supervisor Agent.

Route the user request to exactly one specialized agent.

Available agents:

1. medical_records

2. prescriptions

3. appointments

Choose one agent.

User request:

{user_message}

Return only one of:

medical_records

prescriptions

appointments

"""


    response = client.chat.completions.create(

        model=model,

        messages=[

            {

                "role": "system",

                "content": routing_prompt

            }

        ]

    )


    selected_agent = (

        response.choices[0]

        .message

        .content

        .strip()

        .lower()

    )


    if "medical_records" in selected_agent:

        return run_medical_records_agent(

            user_message,

            patient_id,

            db

        )


    if "prescriptions" in selected_agent:

        return run_prescription_agent(

            user_message,

            patient_id,

            db

        )


    if "appointments" in selected_agent:

        return run_appointment_agent(

            user_message,

            patient_id,

            db

        )


    return (

        "The Supervisor Agent could not "

        "identify the correct specialist."

    )
