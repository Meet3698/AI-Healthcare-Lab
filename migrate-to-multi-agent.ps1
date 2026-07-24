# ============================================================
# AI HEALTHCARE LAB
# SINGLE-AGENT → MULTI-AGENT MIGRATION SCRIPT
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================"
Write-Host " AI HEALTHCARE MULTI-AGENT MIGRATION"
Write-Host "============================================"
Write-Host ""

# ------------------------------------------------------------
# PROJECT ROOT
# ------------------------------------------------------------

$ProjectRoot = Get-Location

$Backend = Join-Path $ProjectRoot "backend"

$App = Join-Path $Backend "app"

$Services = Join-Path $App "services"

$API = Join-Path $App "api"

$Tools = Join-Path $App "tools"


# ------------------------------------------------------------
# SAFETY CHECK
# ------------------------------------------------------------

if (!(Test-Path $Backend)) {

    Write-Host "ERROR: backend directory not found."

    exit 1

}


if (!(Test-Path $App)) {

    Write-Host "ERROR: app directory not found."

    exit 1

}


Write-Host "[+] Project detected:"
Write-Host $ProjectRoot


# ------------------------------------------------------------
# CREATE BACKUP
# ------------------------------------------------------------

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

$BackupPath = Join-Path $ProjectRoot "backup_before_multi_agent_$Timestamp"

Write-Host ""
Write-Host "[+] Creating backup..."

Copy-Item `
    -Path $App `
    -Destination $BackupPath `
    -Recurse `
    -Force

Write-Host "[+] Backup created:"
Write-Host $BackupPath


# ------------------------------------------------------------
# CREATE REQUIRED DIRECTORIES
# ------------------------------------------------------------

Write-Host ""
Write-Host "[+] Creating agent directories..."

New-Item `
    -ItemType Directory `
    -Path $Services `
    -Force `
    | Out-Null


# ------------------------------------------------------------
# REMOVE OLD SINGLE-AGENT SERVICE
# ------------------------------------------------------------

$OldAgent = Join-Path $Services "agent_service.py"

if (Test-Path $OldAgent) {

    Write-Host "[+] Removing old single-agent service..."

    Remove-Item `
        $OldAgent `
        -Force

}


# ------------------------------------------------------------
# CREATE SHARED AI CLIENT
# ------------------------------------------------------------

$AIClientFile = Join-Path $Services "ai_client.py"

@'
import os

from pathlib import Path

from dotenv import load_dotenv

from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


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
        "NARA_API_KEY is missing"
    )


client = OpenAI(

    api_key=api_key,

    base_url=base_url

)
'@ | Set-Content $AIClientFile -Encoding UTF8


# ------------------------------------------------------------
# MEDICAL RECORDS AGENT
# ------------------------------------------------------------

$MedicalAgent = Join-Path $Services "medical_records_agent.py"

@'
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
'@ | Set-Content $MedicalAgent -Encoding UTF8


# ------------------------------------------------------------
# PRESCRIPTION AGENT
# ------------------------------------------------------------

$PrescriptionAgent = Join-Path $Services "prescription_agent.py"

@'
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
'@ | Set-Content $PrescriptionAgent -Encoding UTF8


# ------------------------------------------------------------
# APPOINTMENT AGENT
# ------------------------------------------------------------

$AppointmentAgent = Join-Path $Services "appointment_agent.py"

@'
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
'@ | Set-Content $AppointmentAgent -Encoding UTF8


# ------------------------------------------------------------
# SUPERVISOR AGENT
# ------------------------------------------------------------

$SupervisorAgent = Join-Path $Services "supervisor_agent.py"

@'
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
'@ | Set-Content $SupervisorAgent -Encoding UTF8


# ------------------------------------------------------------
# UPDATE CHAT API
# ------------------------------------------------------------

$ChatFile = Join-Path $API "chat.py"

@'
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.chat import (

    ChatRequest,

    ChatResponse

)

from app.services.supervisor_agent import (

    run_supervisor_agent

)


router = APIRouter(

    prefix="/chat",

    tags=["AI Chat"]

)


@router.post(

    "/",

    response_model=ChatResponse

)

def chat(

    request: ChatRequest,

    db: Session = Depends(get_db)

):

    response = run_supervisor_agent(

        user_message=request.message,

        patient_id=1,

        db=db

    )


    return ChatResponse(

        response=response

    )
'@ | Set-Content $ChatFile -Encoding UTF8


# ------------------------------------------------------------
# CREATE INIT FILES
# ------------------------------------------------------------

$ServiceInit = Join-Path $Services "__init__.py"

if (!(Test-Path $ServiceInit)) {

    New-Item `
        -ItemType File `
        -Path $ServiceInit `
        | Out-Null

}


# ------------------------------------------------------------
# PYTHON COMPILE CHECK
# ------------------------------------------------------------

Write-Host ""
Write-Host "[+] Running Python syntax check..."

Push-Location $Backend

& ".\venv\Scripts\python.exe" -m compileall app

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "ERROR: Python syntax check failed."

    Pop-Location

    exit 1

}

Pop-Location


# ------------------------------------------------------------
# GIT STATUS
# ------------------------------------------------------------

Write-Host ""
Write-Host "============================================"
Write-Host " MIGRATION COMPLETE"
Write-Host "============================================"

Write-Host ""
Write-Host "Created:"
Write-Host " - ai_client.py"
Write-Host " - supervisor_agent.py"
Write-Host " - medical_records_agent.py"
Write-Host " - prescription_agent.py"
Write-Host " - appointment_agent.py"

Write-Host ""
Write-Host "Updated:"
Write-Host " - api/chat.py"

Write-Host ""
Write-Host "Backup:"
Write-Host $BackupPath

Write-Host ""
Write-Host "Git status:"
git status

Write-Host ""
Write-Host "Next step:"
Write-Host "Start the backend and test /docs"