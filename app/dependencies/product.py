import logging

from fastapi import Depends

from app.core.logging import get_logger
from app.services.product_service import ProductService


def get_product_logger() -> logging.Logger:
    return get_logger("app.services.product_service")


def get_product_service(
    logger: logging.Logger = Depends(get_product_logger)
) -> ProductService:

    return ProductService(
        logger=logger
    )