from app.exceptions.user import UserNotFoundException
from app.repositories.user_repository import UserRepository
from app.models.user import (
    UserRequest,
    UserResponse,
    UserDetailResponse
)
import logging

class UserService:

    def __init__(self, repository: UserRepository, logger:logging.Logger):
        self.repository = repository
        self.logger = logger
        self.logger.info("UserService initialized")

    def get_user(self, user_id: int) -> UserDetailResponse:

        self.logger.info("Getting user with ID: %d", user_id)
        user = self.repository.get_user(user_id)
        return UserDetailResponse(
            user_id=user["user_id"],
            name=user["name"],
            age=user["age"],
            email=user["email"]
        )

    def delete_user(self, user_id: int) -> None:
        # Business validation
        if user_id <= 0:
            self.logger.error("User with ID %d not found", user_id)
            raise UserNotFoundException(user_id)

        self.logger.info("Deleting user with ID: %d", user_id)
        self.repository.delete_user(user_id)

    def create_user(self, user: UserRequest) -> UserResponse:
        # Business logic
        self.logger.info("Creating user with name: %s", user.name)
        user_created = self.repository.create_user(user)
        return UserResponse(user_id=user_created.id)

    def update_user(self, user_id: int, user: UserRequest) -> UserResponse:
        # Business logic
        self.logger.info("Updating user with ID: %d", user_id)
        user_updated = self.repository.update_user(user_id, user)
        return UserResponse(user_id=user_updated.id)