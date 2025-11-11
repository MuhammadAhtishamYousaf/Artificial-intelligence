
from pydantic import BaseModel
from fastapi import FastAPI, Query
app=FastAPI(
    name="Post Request",
    description="Learning post request."
)

class User(BaseModel):
    name:str 
    age:int

class UserResponse(BaseModel):
    user_id:int 
    status:str 


@app.post("/get_user/{user_name}",response_model=UserResponse)
def post_request(user:User,user_id:int=Query(...,title="User ID",description="Enter the user id",example=2,gt=0,lt=5)):
    return {"status":"user cteated","user_id": user_id}



@app.put("/update-user/{user_id}",response_model=UserResponse)
def update_user(user_id:int, user:User):
    return {"status":"user updated","user_id":user_id}


@app.delete("/delete-user/{user_id}",response_model=UserResponse)
def delete_user(user_id:int):
    return {"status":"user deleted","user_id":user_id}