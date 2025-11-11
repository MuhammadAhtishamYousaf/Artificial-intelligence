import json, os 
from uuid import uuid4 
from typing import cast 
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from datetime import datetime, UTC

from fastapi import FastAPI,HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from openai.types.responses import ResponseTextDeltaEvent
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
    Agent,
    Runner,
    function_tool,
    ModelProvider
)

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

external_client=AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config=RunConfig(
    model=model,
    model_provider=cast(ModelProvider,external_client), # satisfy type checker
    tracing_disabled=True 
)

app=FastAPI(
    title="ChatBot",
    description="A FastAPI Based api for a chatbot in the daca toturial.",
    version="0.1.0"
)

#Add cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Metadata(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    session_id: str = Field(default_factory=lambda: str(uuid4()))


# class Message(BaseModel):
#     user_id: str
#     question: str
#     metadata: Metadata | None = None
#     tags: list[str] | None = None


class Message(BaseModel):
    user_id: int
    question: str 
    # metadata= Metadata | None = None
    # tags= list[str] | None = None


class Response(BaseModel):
    user_id: str
    reply: str
    metadata: Metadata

@function_tool
def get_current_time() ->str:
    """Returns the current time in UTC."""
    return datetime.now().strftime(format="%Y-%m-%d %H:%M:%S UTC")


# print(get_current_time())

chat_agent=Agent(
    name="ChatAgent",
    instructions="You are a helpful chatbot. Respond to user messages in a friendly and informative way. If the user asks for the time, use the get_current_time tool.",
    tools=[get_current_time],  # Add the time tool
    model=model
)


@app.get("/")
async def root():
    return {"message":"Welcom Muhammad Ahtisham.Access /docs for the API Documentation."}


# Post endpoint with chating
@app.post("/chat", response_model=Response)
async def chat(message: Message):
    if not message.question.strip():
        raise HTTPException(status_code=400,detail="Message cannot be empty")
    
    # use openai agents sdk to response
    result=await Runner.run(
        starting_agent=chat_agent,
        input=message.question,
        run_config=config
    )
    response=result.final_output
    return Response(
        user_id=str(message.user_id),
        reply=response,
        metadata=Metadata()  # auto-generates timestamp & session_id
    )

#streaming the response
async def stream_response(message:Message):
    result=Runner.run_streamed(chat_agent,input=message.question,run_config=config)
    async for event in result.stream_events():
        if event.type=="raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
            print(event.data.delta, end="",flush=True)
            #Serialize dictionary to json string 
            chunk=json.dumps({"chunk":event.data.delta})
            yield f"data: {chunk}\n\n"

@app.post("/chat/stream",response_model=Response)
async def chat_stream(message:Message):
    if not message.question.strip():
        raise HTTPException(status_code=400,detail="Question cannot be empty")
    
    return StreamingResponse(
        content=stream_response(message),
        media_type="text/event-stream"
    )