from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Java Generator Running"}

@app.get("/generate")
def generate(prompt: str):

    command = f"ollama run deepseek-coder '{prompt}'"

    result = subprocess.getoutput(command)

    return {"response": result}