from fastapi import APIRouter, Depends, status

from app.models.user import (
    UserRequest,
    UserResponse,
    UserDetailResponse,
    LoginRequest,
    LoginResponse
)
from app.dependencies.auth import get_current_user
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
    current_user_id: int = Depends(get_current_user),
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
    current_user_id: int = Depends(get_current_user),
    service=Depends(get_user_service)
):
    return service.create_user(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    current_user_id:int = Depends(get_current_user),
    service=Depends(get_user_service)
):
    return service.delete_user(user_id)

@router.put(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserRequest,
    current_user_id:int =  Depends(get_current_user),
    service=Depends(get_user_service)
):
    return service.update_user(user_id, user)


@router.post("/login", response_model=LoginResponse)
def login(
    login_request: LoginRequest,
    service=Depends(get_user_service)
):
    return service.login(login_request)
