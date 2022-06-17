from fastapi import FastAPI, APIRouter, Response, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.params import Depends
from typing import List
from .. import models
from ..schemas import Product, DisplayProduct, Seller
from .login import get_current_user

router = APIRouter(tags=["product"], prefix="/product")

## Product Endpoints


@router.get("/", response_model=List[DisplayProduct])
async def all_products(response: Response, db: Session = Depends(get_db)):
    response.status_code = status.HTTP_200_OK
    products = db.query(models.Product).all()
    return products


@router.get("/{id}", response_model=DisplayProduct)
async def get_product_by_id(
    response: Response,
    id: int,
    db: Session = Depends(get_db),
    current_user: Seller = Depends(get_current_user),
):
    response.status_code = status.HTTP_200_OK
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )
    return product


@router.post("/")
async def add(response: Response, request: Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price,
        seller_id=request.seller_id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    response.status_code = status.HTTP_201_CREATED
    return new_product


@router.delete("/{id}")
async def delete_product_by_id(
    response: Response, id: int, db: Session = Depends(get_db)
):
    db.query(models.Product).filter(models.Product.id == id).delete(
        synchronize_session=False
    )
    db.commit()
    response.status_code = status.HTTP_200_OK
    return {"message": f"Product with id {id} delete"}


@router.put("/{id}")
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
