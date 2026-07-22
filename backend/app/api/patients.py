from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.patient import Patient


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.get("/")
def get_patients(
    db: Session = Depends(get_db)
):

    patients = db.query(Patient).all()

    return patients