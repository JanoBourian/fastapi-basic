from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: float

## Removed id product

# class DisplayProduct(Product):
#     class Config:
#         orm_mode = True

class DisplayProduct(BaseModel):
    name: str
    price: float
    
    class Config:
        orm_mode = True
    