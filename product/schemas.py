from pydantic import BaseModel
from typing import Optional


class Seller(BaseModel):
    username: str
    email: str
    password: str


class DisplaySeller(BaseModel):
    username: str
    email: str
    id: int

    class Config:
        orm_mode = True


class Product(BaseModel):
    name: str
    description: str
    price: float
    seller_id: int


class DisplayProduct(BaseModel):
    name: str
    price: float
    seller: DisplaySeller

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    toke_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
