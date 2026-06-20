import os
import requests
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()
# --------------------------------
# CONFIG
# --------------------------------

MODEL_NAME = "gemini-2.5-flash"

# --------------------------------
# LOCAL OLLAMA
# --------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"

# --------------------------------
# GENERATE RESPONSE
# --------------------------------

def generate_response(prompt):

    try:

        # -----------------------------
        # LOCAL MODE
        # -----------------------------

        if os.getenv("ENVIRONMENT") == "LOCAL":

            payload = {

                "model": "tinyllama",

                "prompt": prompt,

                "stream": False,

                "options": {

                    "temperature": 0.1,

                    "num_predict": 200
                }
            }

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

        # -----------------------------
        # PRODUCTION MODE (GEMINI)
        # -----------------------------

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        genai.configure(
            api_key=api_key
        )

        model = genai.GenerativeModel(
            MODEL_NAME
        )

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        print("\nLLM ERROR:")
        print(str(e))

        return ""