from fastapi import FastAPI, Response, status
from .schemas import Product
from . import models
from .database import engine

app = FastAPI()

# Create table
models.Base.metadata.create_all(engine)


@app.post("/product")
async def add(response: Response, product: Product):
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Hello!"}

@app.get("/product")
async def add():
    return {"message": "Hello!"}