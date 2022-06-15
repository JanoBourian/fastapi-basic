from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: float

class DisplayProduct(BaseModel):
    name: str
    price: float
    
    class Config:
        orm_mode = True

class Seller(BaseModel):
    username:str
    email:str
    password:str

class DisplaySeller(BaseModel):
    name:str
    email:str
    
    class Config:
        orm_mode = True