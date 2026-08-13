



from app.models.product import ProductRequest, ProductResponse


def create_product(product: ProductRequest):
    return ProductResponse(
        product_id=1,
        name=product.name,
        price=product.price)

def get_product(product_id: int):
    return ProductResponse(
        product_id=product_id,
        name="Product 1",
        price=100.0
    )