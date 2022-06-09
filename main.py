from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"message": "in a bottle"}

@app.get("/property")
def property():
    return "<h1> This is a property field </h1>"

@app.get("/movies")
def movies():
    return {'movie_list': {'Movie 1', 'Movie 2'}} #That will be a list of items