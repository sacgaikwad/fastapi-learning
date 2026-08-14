import logging
from app.models.user import UserRequest


class UserRepository:

    def __init__(self,logger:logging.Logger):
        self.logger = logger

    def get_user(self, user_id: int):

        self.logger.info("Fetching user with ID from database: %d", user_id)
        # Database access
        return {
            "user_id": user_id,
            "name": "Sachin",
            "age": 30,
            "email": "sachin@gmail.com"
        }

    def delete_user(self, user_id: int):

        # Database delete
        print(f"Deleting user {user_id}")

    def create_user(self, user: UserRequest):

        # Database insert
        print(f"Creating user {user.name}")