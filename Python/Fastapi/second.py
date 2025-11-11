from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime , UTC
from uuid import uuid4

app=FastAPI(
    title="ChatBot",
    description="A FastAPI Based api for a chatbot in the daca toturial.",
    version="0.1.0"
)

#Complex pydantic model
class Metadata(BaseModel):
    timestamp:datetime=Field(default_factory=lambda:datetime.now(tz=UTC))
    session_id:str=Field(default_factory=lambda:str(uuid4()))


class Message(BaseModel):
    user_id:str 
    text:str
    metadata:Metadata
    tags:list[str] | None=None #Optional

class Response(BaseModel):
    user_id:str 
    reply:str 
    metadata: Metadata

#root endpoint 
@app.get("/")
async def greet():
    return {"message":"Welcome Muhammad Ahtisham, May Allah bless you success in both this world and Akhirt."}

# get endpoint with query parameter
@app.get("/users/{user_id}")
async def get_user(user_id:str , role:str |None=None):
    user_info = {"user_id":user_id,"role":role if role else "guest"}
    return user_info

#post endpoint for chating
@app.post("/chat",response_model=Response)
async def chat(message:Message):
    if not message.text.strip():
        raise HTTPException(status_code=400,detail="Message text cannot be empty.")
    reply_text=f"Assalam u Alaikum, {message.user_id}, You said {message.text}. How can I assist you."
    return Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=Metadata() #auto generated timestamp and session id
    )