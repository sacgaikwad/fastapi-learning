from fastapi import Depends
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
import logging
from app.core.logging import get_logger
from sqlalchemy.orm import Session
from app.database.dependencies import get_db


def get_user_logger() -> logging.Logger:
    return get_logger("app.services.user_service")

def get_user_repository(
    logger: logging.Logger = Depends(get_user_logger),
    db: Session = Depends(get_db)
) -> UserRepository:
    return UserRepository(logger=logger, db=db)

def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
    logger: logging.Logger = Depends(get_user_logger)
) -> UserService:

    return UserService(
        repository=repository,
        logger=logger
    )