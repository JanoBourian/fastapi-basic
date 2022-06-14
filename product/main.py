from fastapi import FastAPI, Response, status
from .schemas import Product


app = FastAPI()


@app.post("/product")
def add(response: Response, product: Product):
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Hello!"}
