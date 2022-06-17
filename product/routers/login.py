from fastapi import APIRouter, Response, status, HTTPException
from fastapi.params import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Seller
from ..schemas import Login, TokenData
from config import SECRET_KEY, ALGORITHM, ACCES_TOKEN_EXPIRES_MINUTES
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["authentication"])

# pwd crypto
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encode_jwt


@router.post("/login")
async def login(
    response: Response,
    db: Session = Depends(get_db),
    request: OAuth2PasswordRequestForm = Depends(),
):
    user = (
        db.query(Seller)
        .filter(Seller.username == request.username)
        .filter(Seller.email == request.email)
        .first()
    )

    # Validations
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username not found / invalid email",
        )
    if not pwd_context.verify(request.password, user.password):
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password"
        )

    # Gen JWT Token
    access_token = generate_token(data={"sub": user.username})
    response.status_code = status.HTTP_200_OK
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", "")
        if username is None:
            pass
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
