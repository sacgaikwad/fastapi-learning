import logging

from app.models.product import ProductRequest, ProductResponse

class ProductService:

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def create_product(
        self,
        product: ProductRequest
    ) -> ProductResponse:

        self._logger.info(
            "Creating product with name: %s",
            product.name
        )

        return ProductResponse(
            product_id=1,
            name=product.name,
            price=product.price
        )

    def get_product(
        self,
        product_id: int
    ) -> ProductResponse:

        self._logger.info(
            "Getting product with ID: %d",
            product_id
        )

        return ProductResponse(
            product_id=product_id,
            name="Product 1",
            price=100.0
        )