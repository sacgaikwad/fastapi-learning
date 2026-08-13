from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from app.services import user_service

from app.models.user import (
    UserRequest,
    UserResponse,
    UserDetailResponse
)

from app.exceptions.user import UserNotFoundException

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/{user_id}",
    response_model=UserDetailResponse,
        
)
def get_user(user_id: int):

    if user_id <= 0:
        raise UserNotFoundException(user_id)

    return UserDetailResponse(
        user_id=user_id,
        name="Sachin",
        age=30,
        email="sachin@gmail.com"
    )

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserRequest):
    response = user_service.create_user(user)
    return response

@router.delete("/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int):
    if user_id <= 0:
        raise UserNotFoundException(user_id)

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=None
    )