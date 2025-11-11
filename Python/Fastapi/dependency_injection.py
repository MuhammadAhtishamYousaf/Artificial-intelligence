from fastapi import FastAPI, Depends, Query, HTTPException,status
from typing import Annotated 

app:FastAPI=FastAPI(
    title="Dependency Injection",
    description="This API is to learn about dependencty injection",
)

#1 Simple dependency 
def get_simple_goal():
    return {"goal":"We are building AI Agents Workforce"}

@app.get("/get-simple-goal")
def simple_goal(response: Annotated[dict,Depends(get_simple_goal)]):
    return response

#2 dependency with parameters 
def get_goal(username:str = Query(title="username",description="Enter user name to get your goals",example="ahtisham")):
    return {"goal":f"You're goal is to build AI Agents Workforce: {username}"}

@app.get("/get_goal")
def get_goal(response: Annotated[dict,Depends(get_goal)]):
    return response

# 3. Dependency with query parameters 
def dependency_login(username:str=Query(None),password:str=Query(None)):
    if username=="admin" and password=="admin":
        return {"message":"login successful"}
    else:
        return {"message":"login failed"}
    
@app.get("/signin")
def login_api(user_status:Annotated[dict,Depends(dependency_login)]):
    return user_status

# 4 Multiple dependencies
def dependency1(num:int):
    num=int(num)
    num+=1
    return num

def dependency2(num:int):
    num=int(num)
    num+=2
    return num

@app.get("/main/{num}")
def get_main(num:int,num1: Annotated[int,Depends(dependency1)], num2:Annotated[int, Depends(dependency2)]):
    #assuming you want to use num1 and num2 in some way
    #     1    2    3
    total=num+num1+num2
    return f"Ahtisham: {total}"


blogs={
    "1":"Generative AI Blog",
    "2":"Mechine learning Blog",
    "3":"AI Agents Blog",
}

users={
    "8":"Hamza",
    "9":"Daniyal"
}


class GetObjectOrErrorClass():
    def __init__(self,model) ->None:
        self.model=model 

    def __call__(self,id:str):
        obj=self.model.get(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Ojbect ID {id} not found")
        return obj 
    
blog_dependency_obj=GetObjectOrErrorClass(blogs)

@app.get("/blog/{id}")
def get_blog(blog_name: Annotated[str,Depends(blog_dependency_obj)]):
    return blog_name


user_dependency_obj=GetObjectOrErrorClass(users)

@app.get("/users/{id}")
def get_user(user_name: Annotated[str,Depends(user_dependency_obj)]):
    return user_name