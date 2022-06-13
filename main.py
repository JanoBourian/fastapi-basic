from fastapi import FastAPI, status, Response, Form
from typing import Optional, List, Set
from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID
from datetime import date, datetime, time, timedelta


class Event(BaseModel):
    event_id: UUID
    start_date: date
    start_time: datetime
    end_time: datetime
    repeat_time: time
    execute_after: timedelta


class Profile(BaseModel):
    name: str = Field(example="username")
    email: str = Field(example="example@mail.com")
    age: int = Field(example=31)
    info: str | None = None


class Image(BaseModel):
    url: HttpUrl
    name: str


class Product(BaseModel):
    name: str
    price: float = Field(
        title="Price of the item",
        description="This would be the price of the item being added",
        gt=0,
    )
    discount_percentage: float
    discounted_price: float = 0.0
    tags: Set[str]
    image: List[Image]

    class Config:
        schema_extra = {
            "example": {
                "name": "speakers",
                "price": 19.99,
                "discount_percentage": 0.04,
                "discounted_price": 0.0,
                "tags": ["speakers"],
                "image": [
                    {
                        "url": "https://pixabay.com/es/photos/cabello-rosado-peinado-mujer-1450045/",
                        "name": "first image",
                    },
                    {
                        "url": "https://pixabay.com/es/photos/mujer-modelo-peinado-maquillaje-2537564/",
                        "name": "usage",
                    },
                ],
            }
        }


class Offer(BaseModel):
    name: str
    description: str
    discount_percentage: float
    products: Set[Product]


class User(BaseModel):
    name: str = Field(example="janobourian")
    email: str = Field(example="janobourian@mail.com")


app = FastAPI()


@app.post(
    "/login",
    tags=["login", "user"],
    summary="Login with form",
    description="Endpoint to recive username and password",
    response_description="Return exit success",
)
def login(response: Response, username: str = Form(...), password: str = Form(...)):
    response.status_code = status.HTTP_201_CREATED
    return {"username": username, "password": password}


@app.get(
    "/",
    tags=["index"],
    summary="The index route",
    description="Return a little regards",
    response_description="Message",
)
def index(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"message": "in a bottle"}


@app.get(
    "/property/{id}",
    tags=["property", "id"],
    summary="Retrieve property by id",
    description="Take id value and return its properties",
    response_description="Message with the property id",
)
def property(id: int, response: Response):
    response.status_code = status.HTTP_200_OK
    return {"message": f"Property by id number {id}"}


@app.get(
    "/profile/{username}",
    tags=["profile", "username"],
    summary="Retrieve profile by username",
    response_description="Message with the profile",
)
def profile(username: str, response: Response):
    """
    Simulates the profiles
    """
    response.status_code = status.HTTP_200_OK
    return {"message": f"This is a profile page for user {username}"}


@app.get(
    "/movies",
    tags=["movies"],
    summary="Check all movies availables",
    description="Return a list of movies availables",
    response_description="JSON dict",
)
def movies(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"movie_list": {"Movie 1", "Movie 2"}}  # That will be a list of items


@app.get(
    "/user/admin",
    tags=["user", "admin"],
    summary="Return admin info",
    description="This endpoint retrieve the admin contact info",
    response_description="A JSON dict with contact info of our admin",
)
def admin(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"message": "Admin page"}


@app.get(
    "/user/{username}",
    tags=["user", "username"],
    summary="Return username info",
    description="This endpoint retrieve the username contact info",
    response_description="A JSON dict with contact info of a specific username",
)
def profile(username: str, response: Response):
    response.status_code = status.HTTP_200_OK
    return {"message": f"username {username}"}


@app.get(
    "/products",
    tags=["id", "price"],
    summary="Retrieve id and price of a product",
    description="Return the id and price",
    response_description="A JSON dict with product price and id",
)
def products(response: Response, id: int = None, price: float = None):
    response.status_code = status.HTTP_200_OK
    return {"message": f"Product with an id: {id} and price {price}"}


@app.get(
    "/profile/{userid}/comments",
    tags=["userid", "commentid"],
    summary="Return info",
    description="Return a list of comments",
    response_description="A JSON dict with the info",
)
async def profile(response: Response, userid: int = None, commentid: int = None):
    response.status_code = status.HTTP_200_OK
    return {
        "message": f"Profile page for user with user id {userid} and comment with {commentid}"
    }


@app.post(
    "/adduser",
    tags=["user", "add"],
    summary="Add a user",
    description="Endpoint that creates and adds a user",
    response_description="A JSON dict with a successfull message",
)
async def adduser(response: Response, profile: Profile):
    response.status_code = status.HTTP_201_CREATED
    return profile


@app.post(
    "/addproduct/{product_id}",
    tags=["product", "add", "product_id", "store_id", "category"],
    summary="Add a product info",
    description="Add name, price and discount with its rules",
    response_description="Return a new info about the created product",
)
async def addproduct(
    response: Response,
    product: Product,
    product_id: int,
    store_id: int = None,
    category: str = None,
):
    product.discounted_price = round(
        product.price * (1 - product.discount_percentage), 3
    )
    response.status_code = status.HTTP_201_CREATED
    return {
        "product_id": product_id,
        "product": product,
        "store_id": store_id,
        "category": category,
    }


@app.post(
    "/purchase",
    tags=["product", "purchase", "user"],
    summary="Add a purchase by user",
    description="Add a purchase for certain user",
    response_description="Return dummy info",
)
async def purchase(response: Response, user: User, product: Product):
    response.status_code = status.HTTP_201_CREATED
    return {"user": user, "product": product}


@app.post(
    "/addoffer",
    tags=["offer"],
    summary="Add an offer",
    description="Enpoint that added an offer",
    response_description="Return a success message",
)
async def addoffer(response: Response, offer: Offer):
    response.status_code = status.HTTP_201_CREATED
    return offer


@app.post(
    "/addevent",
    tags=["event"],
    summary="Add event",
    description="Enpoint that add event",
    response_description="Return a success message",
)
async def addevent(response: Response, event: Event):
    response.status_code = status.HTTP_201_CREATED
    return event
