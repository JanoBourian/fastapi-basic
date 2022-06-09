from fastapi import FastAPI, status, Response
from typing import Optional

app = FastAPI()

@app.get("/", 
         tags = ["index"],
         summary = "The index route", 
         description = "Return a little regards",
         response_description = "Message")
def index(response:Response):
    response.status_code = status.HTTP_200_OK
    return {"message": "in a bottle"}

@app.get("/property/{id}",
         tags = ["property", "id"],
         summary = "Retrieve property by id", 
         description = "Take id value and return its properties",
         response_description = "Message with the property id")
def property(id: int, response:Response):
    response.status_code = status.HTTP_200_OK
    return {"message": f"Property by id number {id}"}

@app.get('/profile/{username}',
         tags = ["profile", "username"],
         summary = "Retrieve profile by username",
         response_description = "Message with the profile")
def profile(username: str, response:Response):
    """ 
    Simulates the profiles
    """
    response.status_code = status.HTTP_200_OK
    return {"message": f"This is a profile page for user {username}"}

@app.get("/movies",
         tags = ["movies"], 
         summary = "Check all movies availables",
         description = "Return a list of movies availables",
         response_description = "JSON dict")
def movies(response:Response):
    response.status_code = status.HTTP_200_OK
    return {'movie_list': {'Movie 1', 'Movie 2'}} #That will be a list of items

@app.get("/user/admin", 
         tags = ["user", "admin"],
         summary = "Return admin info", 
         description = "This endpoint retrieve the admin contact info", 
         response_description = "A JSON dict with contact info of our admin")
def admin(response:Response):
    response.status_code = status.HTTP_200_OK
    return {"message": "Admin page"}

@app.get("/user/{username}", 
         tags = ["user", "username"],
         summary = "Return username info", 
         description = "This endpoint retrieve the username contact info", 
         response_description = "A JSON dict with contact info of a specific username")
def admin(username:str, response:Response):
    response.status_code = status.HTTP_200_OK
    return {"message": f"username {username}"}