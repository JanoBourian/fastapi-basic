# fastapi-basic
A basic course of FastAPI topics and knowledges

## Start FastAPI
    - uvicorn main:app --reload

## Path and Query Parameters
    - Dynamic value "/propery/{id}"
    - Documentation with "/docs" or "/redoc" and remember that you can use: 
        - tags
        - summary
        - description
        - response_description
        - status.HTTP_200_OK
    - Ordering Routes or paths: The order is so much important
    - Query parameters by default; You should remember the typing is so important
    - Query parameters and path parameters can be in the same function
    - None make more sense like zero or empty value

## Request Body and Pydantic
    - POST method
    - Request Model: pydantic
    - Past one or more Model
    - Add metadata info
    - Nesting Python Datatypes in a Models
    - Provide example data as a class inside the pydantic Model
    - Provide exampla data using fields
    - Time data types
    - Forms 

## Connecting to the database
    - SQLAlchemy
    - SQLite
    - Creating a project 
    - Creating a connection : Check this link or advanced setup https://fastapi.tiangolo.com/tutorial/sql-databases/
    - Creating a model
    - Using Table Plus

## Generate requirements.txt
    - pip freeze >> requirements.txt

## Requirements.txt
    - pip install fastapi
    - pip install uvicorn
    - pip install requests
    - pip install pytest
    - pip install black
    - pip install python-multipart
    - pip install sqlalchemy