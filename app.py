from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import requests
import os

app = FastAPI()

API_KEY = os.getenv("GROQ_API_KEY")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/chat")
async def chat(request: Request):

    body = await request.json()
    message = body.get("message")

    if not message:
        return JSONResponse({"error": "Message required"}, status_code=400)

    if len(message) > 2000:
        return JSONResponse({"error": "Message too large"}, status_code=400)

    prompt = f"""
You are a Java and Spring Boot expert.

User request:
{message}

If user asks for code:
- return clean formatted code
- explain briefly
"""

    try:

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        data = response.json()

        if "error" in data:
            return {"error": data["error"]}

        return {
            "reply": data["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return {"error": str(e)}