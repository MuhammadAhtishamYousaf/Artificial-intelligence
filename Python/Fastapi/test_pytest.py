import pytest 
from fastapi.testclient import TestClient 
from second import app

client=TestClient(app)

# Test the greeting endpoint
def test_greeting():
    response=client.get("/")
    assert response.status_code==200
    assert response.json()=={"message":"Welcome Muhammad Ahtisham, May Allah bless you success in both this world and Akhirt."}

# test the /users/{user_id} endpoint
def test_get_user():
    # response=client.get("/users/ahtisham?role=admin")
    # assert response.status_code==200
    # assert response.json()=={"user_id":"ahtisham","role":"admin"}
    
    response=client.get("/users/bob")
    assert response.status_code==200
    assert response.json()=={"user_id":"bob","role":"guest"}

@pytest.mark.asyncio
async def test_chat():
    # valid data 
    request_data={
        "user_id":"ahtisham",
        "text":"Hello",
        "metadata":{
            "timestamp": "2025-04-06T12:00:00Z",
            "session_id": "123e4567-e89b-12d3-a456-426614174000"
        },
        "tags":["greeting"]
    }
    response=client.post("/chat/",json=request_data)
    assert response.status_code==200 
    assert response.json()["user_id"]=="ahtisham"
    # reply_text=f"Assalam u Alaikum, {message.user_id}, You said {message.text}. How can I assist you."
    assert response.json()["reply"]=="Assalam u Alaikum, ahtisham, You said Hello. How can I assist you."
    # assert "metadata" in response.json()

    
    # Invalid request (empty text)
    # invalid_data = {
    #     "user_id": "bob",
    #     "text": "",
    #     "metadata": {
    #         "timestamp": "2025-04-06T12:00:00Z",
    #         "session_id": "123e4567-e89b-12d3-a456-426614174001"
    #     }
    # }
    # response = client.post("/chat/", json=invalid_data)
    # assert response.status_code == 400
    # assert response.json() == {"detail": "Message text cannot be empty"}