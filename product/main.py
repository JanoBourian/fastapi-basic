from fastapi import FastAPI
from config import config
from . import models
from .database import engine
from .routers import product, seller

app = FastAPI(**config)

# Router
app.include_router(product.router)
app.include_router(seller.router)

# Create table
models.Base.metadata.create_all(engine)
