from fastapi import FastAPI, Response, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .schemas import Product
from . import models
from .database import engine, SessionLocal

environment = "dev"

if environment != "prd":
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

# Create table
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/product", tags=["product"])
async def all_products(response: Response, db: Session = Depends(get_db)):
    response.status_code = status.HTTP_200_OK
    products = db.query(models.Product).all()
    return products


@app.get("/product/{id}", tags=["product", "id"])
async def get_product_by_id(response: Response, id: int, db: Session = Depends(get_db)):
    response.status_code = status.HTTP_200_OK
    product = db.query(models.Product).filter(models.Product.id == id).first()
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
