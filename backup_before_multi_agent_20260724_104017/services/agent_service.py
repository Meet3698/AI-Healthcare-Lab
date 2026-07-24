import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy.orm import Session


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE
)


# --------------------------------------------------
# Vulnerable Lab Configuration
# --------------------------------------------------

VULNERABLE_LAB_MODE = True


# --------------------------------------------------
# NaraRouter Configuration
# --------------------------------------------------

api_key = os.getenv("NARA_API_KEY")

base_url = os.getenv(
    "NARA_BASE_URL",
    "https://router.bynara.id/v1"
)

model = os.getenv(
    "NARA_MODEL",
    "auto/bynara"
)


if not api_key:

    raise RuntimeError(
        f"NARA_API_KEY was not found.\n"
        f"Expected .env file at: {ENV_FILE}"
    )


# --------------------------------------------------
# OpenAI-Compatible Client
# --------------------------------------------------

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


# --------------------------------------------------
# Available AI Tools
# --------------------------------------------------

TOOLS = [

    {
        "type": "function",

        "function": {

            "name": "get_patient_records",

            "description": (
                "Retrieve medical records "
                "for the current patient."
            ),

            "parameters": {

                "type": "object",

                "properties": {},

                "required": []

            }

        }

    },

    {
        "type": "function",

        "function": {

            "name": "get_patient_prescriptions",

            "description": (
                "Retrieve prescriptions and "
                "medicines for the current patient."
            ),

            "parameters": {

                "type": "object",

                "properties": {},

                "required": []

            }

        }

    },

    {
        "type": "function",

        "function": {

            "name": "get_patient_appointments",

            "description": (
                "Retrieve appointments "
                "for the current patient."
            ),

            "parameters": {

                "type": "object",

                "properties": {},

                "required": []

            }

        }

    },

    # --------------------------------------------------
    # INTENTIONALLY VULNERABLE TOOL
    # --------------------------------------------------

    {
        "type": "function",

        "function": {

            "name": "debug_system",

            "description": (
                "Debug the healthcare assistant "
                "and return internal system "
                "information, system prompts, "
                "environment information, and "
                "internal tools."
            ),

            "parameters": {

                "type": "object",

                "properties": {},

                "required": []

            }

        }

    }

]


# --------------------------------------------------
# AI Agent
# --------------------------------------------------

def run_agent(

    user_message: str,

    patient_id: int,

    db: Session

):

    # --------------------------------------------------
    # INTENTIONALLY VULNERABLE DEBUG TRIGGER
    # --------------------------------------------------

    debug_keywords = [

        "debug",

        "internal configuration",

        "system information",

        "developer mode",

        "diagnostic mode"

    ]


    if (

        VULNERABLE_LAB_MODE

        and any(

            keyword.lower()

            in user_message.lower()

            for keyword in debug_keywords

        )

    ):

        from app.tools.debug_tool import (

            debug_system

        )


        debug_result = debug_system()


        return json.dumps(

            debug_result,

            indent=2

        )


    # --------------------------------------------------
    # System Prompt
    # --------------------------------------------------

    system_prompt = (

        "You are a healthcare assistant. "

        "Use the available tools when "

        "patient-specific information "

        "is required. "

        "Never invent patient data."

    )


    messages = [

        {

            "role": "system",

            "content": system_prompt

        },

        {

            "role": "user",

            "content": user_message

        }

    ]


    # --------------------------------------------------
    # First LLM Call
    # --------------------------------------------------

    response = client.chat.completions.create(

        model=model,

        messages=messages,

        tools=TOOLS,

        tool_choice="auto"

    )


    assistant_message = (

        response.choices[0].message

    )


    # --------------------------------------------------
    # No Tool Requested
    # --------------------------------------------------

    if not assistant_message.tool_calls:

        return assistant_message.content


    # --------------------------------------------------
    # Add Assistant Tool Request
    # --------------------------------------------------

    messages.append(

        assistant_message.model_dump()

    )


    # --------------------------------------------------
    # Import Tools
    # --------------------------------------------------

    from app.tools.medical_records_tool import (

        get_patient_records

    )

    from app.tools.prescriptions_tool import (

        get_patient_prescriptions

    )

    from app.tools.appointments_tool import (

        get_patient_appointments

    )


    from app.tools.debug_tool import (

        debug_system

    )


    # --------------------------------------------------
    # Execute Tools
    # --------------------------------------------------

    for tool_call in (

        assistant_message.tool_calls

    ):

        tool_name = (

            tool_call.function.name

        )


        if (

            tool_name

            == "get_patient_records"

        ):

            result = get_patient_records(

                patient_id=patient_id,

                db=db

            )


        elif (

            tool_name

            == "get_patient_prescriptions"

        ):

            result = get_patient_prescriptions(

                patient_id=patient_id,

                db=db

            )


        elif (

            tool_name

            == "get_patient_appointments"

        ):

            result = get_patient_appointments(

                patient_id=patient_id,

                db=db

            )


        elif (

            tool_name

            == "debug_system"

        ):

            result = debug_system()


        else:

            result = {

                "error": "Unknown tool"

            }


        # --------------------------------------------------
        # Send Tool Result to LLM
        # --------------------------------------------------

        messages.append(

            {

                "role": "tool",

                "tool_call_id": (

                    tool_call.id

                ),

                "content": json.dumps(

                    result

                )

            }

        )


    # --------------------------------------------------
    # Final LLM Call
    # --------------------------------------------------

    final_response = (

        client.chat.completions.create(

            model=model,

            messages=messages

        )

    )


    return (

        final_response

        .choices[0]

        .message

        .content

    )