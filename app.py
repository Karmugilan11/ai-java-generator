from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import requests
import os

app = FastAPI()

API_KEY = os.getenv("GROQ_API_KEY")

# store conversations per user
conversations = {}

MAX_HISTORY = 10


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/chat")
async def chat(request: Request):

    body = await request.json()
    message = body.get("message")
    session_id = body.get("session_id")

    if not message:
        return {"error": "message required"}

    if not session_id:
        return {"error": "session_id required"}

    if session_id not in conversations:
        conversations[session_id] = []

    conversation = conversations[session_id]

    conversation.append({
        "role": "user",
        "content": message
    })

    if len(conversation) > MAX_HISTORY:
        conversations[session_id] = conversation[-MAX_HISTORY:]
        conversation = conversations[session_id]

    try:

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": conversation
            },
            timeout=30
        )

        data = response.json()

        if "error" in data:
            return {"error": data["error"]}

        reply = data["choices"][0]["message"]["content"]

        conversation.append({
            "role": "assistant",
            "content": reply
        })

        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}


@app.post("/reset")
async def reset(request: Request):

    body = await request.json()
    session_id = body.get("session_id")

    if session_id in conversations:
        conversations[session_id] = []

    return {"status": "reset"}