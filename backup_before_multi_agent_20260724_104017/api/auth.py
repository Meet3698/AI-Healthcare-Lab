from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.user import User

)

@router.post("/register")
def register(

    request: RegisterRequest,

    db: Session = Depends(get_db)

):

    existing_user = (

        db.query(User)

        .filter(

            User.email == request.email

        )

        .first()

    )


    if existing_user:

        raise HTTPException(

            status_code=400,

            detail="Email already registered"

        )


    hashed_password = hash_password(

        request.password

    )


    user = User(

        email=request.email,

        password_hash=hashed_password

    )


    db.add(user)

    db.commit()

    db.refresh(user)


    return {

        "message": (
            "User registered successfully"
        ),

        "user_id": user.id

    }


@router.post(

    "/login",

    response_model=TokenResponse

)

def login(

    request: LoginRequest,

    db: Session = Depends(get_db)

):

    user = (

        db.query(User)

        .filter(

            User.email == request.email

        )

        .first()

    )


    if not user:

        raise HTTPException(

            status_code=401,

            detail="Invalid credentials"

        )


    if not verify_password(

        request.password,

        user.password_hash

    ):

        raise HTTPException(

            status_code=401,

            detail="Invalid credentials"

        )


    token = create_access_token(

        user.id

    )


    return {

        "access_token": token,

        "token_type": "bearer"

    }