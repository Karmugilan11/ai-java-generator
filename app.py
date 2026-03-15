from fastapi import FastAPI
import requests

app = FastAPI()

API_KEY = "your_deepseek_api_key"

@app.get("/")
def home():
    return {"message": "AI Code Assistant Running"}

@app.get("/analyze")
def analyze(code:str):

    prompt = f"""
    Analyze the following code.
    Find bugs and suggest corrections.

    Code:
    {code}
    """

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-coder",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    return response.json()