import logging
from app.database.models.user import User
from app.exceptions.user import UserNotFoundException
from app.models.user import UserRequest
from sqlalchemy.orm import Session

class UserRepository:

    def __init__(self,logger:logging.Logger,db:Session):
        self.logger = logger
        self.db = db

    def get_user(self, user_id: int):

        self.logger.info("Fetching user with ID from database: %d", user_id)

        user = self.db.query(User).filter(User.id == user_id).first()

        if user is None:
            self.logger.error("User with ID %d not found", user_id)
            raise UserNotFoundException(user_id)

        # Database access
        return {
            "user_id": user_id,
            "name": user.name,
            "age": user.age,
            "email": user.email
        }

    def delete_user(self, user_id: int):

        self.logger.info("Deleting user with ID from database: %d", user_id)

        user = self.db.query(User).filter(User.id == user_id).first()

        if user is None:
            self.logger.error("User with ID %d not found", user_id)
            raise UserNotFoundException(user_id)
        try:
            self.db.delete(user)
            self.db.commit()
            self.logger.info("User with ID %d deleted successfully.",user_id)

        except Exception as e:
            self.db.rollback()
            self.logger.error("Error deleting user with ID %d: %s", user_id, str(e))
            raise e

    def create_user(self, user: UserRequest, password_hashed: str):

        self.logger.info("Creating user in database with email: %s",user.email)

        db_user = User(name =user.name, age=user.age, email=user.email, password_hash=password_hashed)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        self.logger.info("User created with ID: %d", db_user.id)
        return db_user


    def update_user(self, user_id:int, user: UserRequest):

        self.logger.info("Updating user with ID from database: %d", user_id)

        db_user = self.db.query(User).filter(User.id == user_id).first()

        if db_user is None:
            raise UserNotFoundException(user_id)

        db_user.name = user.name
        db_user.age = user.age
        db_user.email = user.email

        self.db.commit()
        self.db.refresh(db_user)

        self.logger.info("User with ID %d updated successfully.", user_id)
        return db_user

    def get_user_by_email(self, email: str):

        self.logger.info("Fetching user with email from database: %s", email)

        user = self.db.query(User).filter(User.email == email).first()

        if user is None:
            self.logger.error("User with email %s not found", email)
            raise UserNotFoundException(email)

        return {
            "user_id": user.id,
            "name": user.name,
            "age": user.age,
            "email": user.email,
            "password_hash": user.password_hash
        }