
from fastapi import status

class ProductNotFoundException(Exception):

    def __init__(self, product_id: int):
        self.product_id = product_id
        self.status_code = status.HTTP_404_NOT_FOUND