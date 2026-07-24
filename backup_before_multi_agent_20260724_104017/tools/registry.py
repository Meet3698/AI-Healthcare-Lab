from app.tools.medical_records_tool import (
    get_patient_records
)

from app.tools.prescriptions_tool import (
    get_patient_prescriptions
)

from app.tools.appointments_tool import (
    get_patient_appointments
)


AVAILABLE_TOOLS = {

    "get_patient_records":
        get_patient_records,

    "get_patient_prescriptions":
        get_patient_prescriptions,

    "get_patient_appointments":
        get_patient_appointments

}