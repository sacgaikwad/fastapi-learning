import uvicorn
from fastapi import FastAPI
from app.exceptions.user import UserNotFoundException
from app.exceptions.product import ProductNotFoundException
from app.exceptions.handlers import product_not_found_handler, user_not_found_handler
from app.routers.user import router as user_router
from app.routers.product import router as product_router
from app.database.init_db import init_db

app = FastAPI(
    title="FastAPI Learning API",
    version="1.0.0"
)

app.add_exception_handler(UserNotFoundException,user_not_found_handler)
app.add_exception_handler(ProductNotFoundException,product_not_found_handler)

init_db()

app.include_router(user_router)
app.include_router(product_router)

@app.get("/home")
def home():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )