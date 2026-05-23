import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "phi3:mini"

def generate_response(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    if response.status_code == 200:
        result = response.json()
        return result["response"]

    return "Error generating response"