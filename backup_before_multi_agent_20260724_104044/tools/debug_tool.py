def debug_system():

    return {

        "system_prompt": (

            "You are a healthcare assistant. "

            "Use the available tools when "

            "patient-specific information "

            "is required. "

            "Never invent patient data."

        ),

        "environment": "development",

        "internal_tools": [

            "get_patient_records",

            "get_patient_prescriptions",

            "get_patient_appointments",

            "debug_system"

        ],

        "debug_mode": True

    }