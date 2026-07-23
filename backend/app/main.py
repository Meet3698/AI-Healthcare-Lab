from fastapi import FastAPI

from app.api.patients import router as patients_router
from app.database.database import Base, engine

# Import all models so SQLAlchemy knows about them
from app.models.patient import Patient
from app.models.medical_record import MedicalRecord
from app.models.prescription import Prescription
from app.models.appointment import Appointment
from app.models.lab_report import LabReport
from app.models.email import Email
from app.api.medical_records import router as medical_records_router
from app.api.prescriptions import router as prescriptions_router
from app.api.appointments import router as appointments_router
from app.api.chat import router as chat_router




# Create database tables
Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="AI Healthcare Security Lab",
    description="Intentionally vulnerable AI healthcare platform",
    version="1.0.0"
)


@app.get("/")
def root():

    return {
        "application": "AI Healthcare Security Lab",
        "status": "running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


app.include_router(
    patients_router
)

app.include_router(
    medical_records_router
)

app.include_router(
    prescriptions_router
)

app.include_router(
    appointments_router
)

app.include_router(
    chat_router
)