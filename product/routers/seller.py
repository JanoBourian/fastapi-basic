from fastapi import FastAPI, APIRouter, Response, status
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.params import Depends
from .. import models
from ..schemas import Seller, DisplaySeller
from passlib.context import CryptContext

router = APIRouter(tags=["seller"], prefix="/seller")

# pwd crypto
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

## Seller endpoints


@router.post("/seller", tags=["seller"], response_model=DisplaySeller)
async def create_seller(
    response: Response, request: Seller, db: Session = Depends(get_db)
):
    hash_pwd = pwd_context.hash(request.password)
    response.status_code = status.HTTP_201_CREATED
    new_seller = models.Seller(
        username=request.username, email=request.email, password=hash_pwd
    )
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
