from fastapi import APIRouter, Depends, status

from app.models.user import (
    UserRequest,
    UserResponse,
    UserDetailResponse
)

from app.dependencies.user import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get(
    "/{user_id}",
    response_model=UserDetailResponse
)
def get_user(
    user_id: int,
    service=Depends(get_user_service)
):
    return service.get_user(user_id)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: UserRequest,
    service=Depends(get_user_service)
):
    return service.create_user(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    service=Depends(get_user_service)
):
    return service.delete_user(user_id)