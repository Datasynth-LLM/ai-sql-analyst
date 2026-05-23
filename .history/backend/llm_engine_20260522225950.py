import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "tinyllama"

def generate_response(prompt):

    payload = {

        "model": MODEL_NAME,

        "prompt": prompt,

        "stream": False,

        "options": {

            "temperature": 0.1,

            "num_predict": 120
        }
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        result = response.json()

        return result.get(
            "response",
            ""
        )

    except Exception as e:

        return f"LLM Error: {str(e)}"