import os
import requests

from dotenv import load_dotenv
from google import genai

load_dotenv()

# --------------------------------
# CONFIG
# --------------------------------

MODEL_NAME = "gemini-2.5-flash"

OLLAMA_URL = "http://localhost:11434/api/generate"


# --------------------------------
# LOCAL OLLAMA
# --------------------------------

def _run_ollama(prompt):

    payload = {
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 300
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result.get("response", "")


# --------------------------------
# GEMINI
# --------------------------------

def _run_gemini(prompt):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found.")

    client = genai.Client(
        api_key=api_key
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    # Preferred SDK response
    if hasattr(response, "text") and response.text:
        return response.text.strip()

    # Fallback for SDK response structure
    try:

        if (
            response.candidates
            and response.candidates[0].content.parts
        ):

            return (
                response
                .candidates[0]
                .content
                .parts[0]
                .text
                .strip()
            )

    except Exception:
        pass

    return ""


# --------------------------------
# PUBLIC FUNCTION
# --------------------------------

def generate_response(prompt):

    try:

        environment = os.getenv(
            "ENVIRONMENT",
            "LOCAL"
        ).upper()

        # Local development
        if environment == "LOCAL":
            return _run_ollama(prompt)

        # Production / Gemini
        return _run_gemini(prompt)

    except Exception as e:

        print("\n========== LLM ERROR ==========")
        print(str(e))
        print("================================\n")

        return ""