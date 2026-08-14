from fastapi import APIRouter, Depends,status
from fastapi.responses import JSONResponse
from app.models.product import ProductRequest, ProductResponse
from app.services.product_service import ProductService
from app.dependencies.product import get_product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK
)
def get_product(product_id: int, product_service: ProductService = Depends(get_product_service)):
    if product_id <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Product not found"}
        )
    return product_service.get_product(product_id)

@router.post("",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(product: ProductRequest, product_service: ProductService = Depends(get_product_service)):
    return product_service.create_product(product)