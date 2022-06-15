from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .schemas import Product, DisplayProduct
from . import models
from .database import engine, SessionLocal
from config import config
from typing import List

app = FastAPI(**config)

# Create table
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/product", tags=["product"], response_model = List[DisplayProduct])
async def all_products(response: Response, db: Session = Depends(get_db)):
    response.status_code = status.HTTP_200_OK
    products = db.query(models.Product).all()
    return products


@app.get("/product/{id}", tags=["product", "id"], response_model = DisplayProduct)
async def get_product_by_id(response: Response, id: int, db: Session = Depends(get_db)):
    response.status_code = status.HTTP_200_OK
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Product with id {id} not found")
    return product


@app.post("/product", tags=["product"])
async def add(response: Response, request: Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name, description=request.description, price=request.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    response.status_code = status.HTTP_201_CREATED
    return new_product


@app.delete("/product/{id}", tags=["product", "id"])
async def delete_product_by_id(
    response: Response, id: int, db: Session = Depends(get_db)
):
    db.query(models.Product).filter(models.Product.id == id).delete(
        synchronize_session=False
    )
    db.commit()
    response.status_code = status.HTTP_200_OK
    return {"message": f"Product with id {id} delete"}


@app.put("/product/{id}", tags=["product", "id"])
async def update(
    response: Response, id: int, request: Product, db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Product with id {id} not found"}
    product.update(request.dict())
    db.commit()
    response.status_code = status.HTTP_200_OK
    return request
