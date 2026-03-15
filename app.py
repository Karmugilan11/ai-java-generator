from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
import os

app = FastAPI()

API_KEY = os.getenv("GROQ_API_KEY")

@app.get("/")
def home():
     return FileResponse("index.html")

@app.get("/analyze")
def analyze(code: str):

    prompt = f"Generate a Spring Boot skeleton project: {code}"

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
            return {"groq_error": data}

        return {
            "ai_response": data["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return {"server_error": str(e)}