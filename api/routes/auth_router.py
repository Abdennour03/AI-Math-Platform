from fastapi import APIRouter, HTTPException

from api.schemas.auth_schema import (
    LoginRequest,
    LoginResponse
)

from api.dependencies import auth_controller


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):

    result = auth_controller.login(
        data.email,
        data.password
    )

    if result is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return result