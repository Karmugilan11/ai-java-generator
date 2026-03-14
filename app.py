from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Java Generator Running"}

@app.get("/generate")
def generate(prompt: str):

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "deepseek-coder",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)

    return response.json()