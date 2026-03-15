from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import requests
import os

app = FastAPI()

API_KEY = os.getenv("GROQ_API_KEY")

# conversation memory
conversation = []

@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/chat")
async def chat(request: Request):

    body = await request.json()
    message = body.get("message")

    if not message:
        return {"error": "message required"}

    # add user message to history
    conversation.append({
        "role": "user",
        "content": message
    })

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
            }
        )

        data = response.json()

        if "error" in data:
            return {"error": data["error"]}

        reply = data["choices"][0]["message"]["content"]

        # save AI reply
        conversation.append({
            "role": "assistant",
            "content": reply
        })

        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}