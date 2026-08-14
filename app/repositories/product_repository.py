import logging
from app.models.product import ProductRequest
from app.models.product import ProductRequest

class ProductRepository:

    def __init__(self,logger:logging.Logger):
        self.logger = logger

    def get_product(self, product_id: int):

        self.logger.info("Fetching product with ID from database: %d", product_id)
        # Database access
        return {
            "product_id": product_id,
            "name": "Sachin",
            "price": 100.0
        }

    def delete_product(self, product_id: int):

        # Database delete
        print(f"Deleting product {product_id}")


    def create_product(self, product: ProductRequest):

        # Database insert
        print(f"Creating product {product.name}")