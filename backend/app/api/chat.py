from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.agents.supervisor_agent import (
    run_supervisor_agent
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(
    user_message: str,
    patient_id: int,
    db: Session = Depends(get_db)
):

    response = run_supervisor_agent(

        user_message=user_message,

        patient_id=patient_id,

        db=db

    )


    return {

        "response": response

    }