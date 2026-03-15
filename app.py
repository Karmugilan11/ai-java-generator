from fastapi import FastAPI
import requests
import os

app = FastAPI()

API_KEY = os.getenv("sk-03903cf9888146fea4e9dd4dac5df5bb")

@app.get("/")
def home():
    return {"message": "AI Code Assistant Running"}

@app.get("/analyze")
def analyze(code: str):

    prompt = f"Generate a Spring Boot skeleton project: {code}"

    try:

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        data = response.json()

        # If API returned error
        if "error" in data:
            return {"deepseek_error": data}

        return {
            "ai_response": data["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return {"server_error": str(e)}