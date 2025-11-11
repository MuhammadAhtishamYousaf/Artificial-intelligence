from pydantic import BaseModel, ValidationError

# Define a simple model
class User(BaseModel):
    id:int 
    name:str 
    email:str 
    age:int |None=None 

# valid data 
user_data={"id":1, "name":"Ahtisham","email":"shammayoa@gmail.com","age":21}
# print(User(user_data))
user=User(**user_data)

# print(user)
# print(user.model_dump())

# Invalid data (will raise an error)
# try:
#     invalid_user = User(id="not_an_int", name="Bob", email="bob@example.com")
# except ValidationError as e:
#     print(e)

# Advanced 
from pydantic import BaseModel, EmailStr,field_validator

# Define a nested model


class Address(BaseModel):
    permanent: str
    temporary: str
    # zip_code: str


class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr  # Built-in validator for email format
    addresses: list[Address]  # List of nested Address models


user_data={
    "id":1,
    "name":"Muhammad Ahtisham",
    "email":"shammayo@gmail.com",
    "addresses":[
        {"permanent":"Badian Road","temporary":"Heir"},
        {"permanent":"Lahore","temporary":"Qasur"}
    ]
}

user=UserWithAddress(**user_data)
# print(user.model_dump())

class Address(BaseModel):
    permanent: str
    temporary: str
    # zip_code: str


class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr  # Built-in validator for email format
    addresses: list[Address]  # List of nested Address models

    @field_validator("name")
    def name_must_be_at_least_two_chars(cls,v):
        if len(v) < 2:
            raise ValueError("Name must be at least two chars.")
        return v
    
try:#test with invalid data

    invalid_user = UserWithAddress(
        id=3,
        name="M",
        email="shammayo@gmail.com",
        addresses=[
            {"permanent":"Badian Road","temporary":"Heir"},
            {"permanent":"Lahore","temporary":"Qasur"},
        ],
    )
except ValidationError as e:
    print(e)