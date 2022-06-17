from fastapi import APIRouter, Response, status, HTTPException
from fastapi.params import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Seller
from ..schemas import Login 


router = APIRouter(prefix="/auth", tags = ["authentication"])

# pwd crypto
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
async def login(request: Login, response:Response, db: Session = Depends(get_db)):
    user = db.query(Seller).filter(Seller.username == request.username).filter(Seller.email == request.email).first()
    
    # Validations
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Username not found / invalid email")
    if not pwd_context.verify(request.password, user.password):
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid password")
    
    # Gen JWT Token
    
    
    response.status_code = status.HTTP_200_OK
    return request