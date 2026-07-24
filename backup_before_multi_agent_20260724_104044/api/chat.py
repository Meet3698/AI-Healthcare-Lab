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
