from fastapi import FastAPI
from pydantic_example1 import BaseModel
from typing import List 

app = FastAPI()

@app.get("/home/{name}")
def hello(name:str) -> str:
    return f"Hello, {name}!"

@app.get("/items")
def get_items(skip:int=0,limit:int=10):
    return [f"skip: {skip}, limit: {limit}"]


# Step 2: Define the input data using a model
class InputData(BaseModel):
    a: float
    b: float

# Step 3: Create an endpoint
@app.post("/add")
def add_numbers(data: InputData):
    result = data.a + data.b
    return {"result": result}


class Temperature(BaseModel):
    celsius: float

@app.post("/convert")
def convert_temperature(temp: Temperature):
    fahrenheit = (temp.celsius * 9/5) + 32
    return {
        "celsius": temp.celsius,
        "fahrenheit": fahrenheit
    }

