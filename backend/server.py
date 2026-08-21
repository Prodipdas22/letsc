import os
import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="LETSC AI API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "name": "LETSC AI"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    if not OPENROUTER_API_KEY:
        return {
            "success": False,
            "error": "OPENROUTER_API_KEY is missing on the server."
        }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://letscomp.netlify.app",
        "X-Title": "LETSC Personal AI"
    }

    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are LETSC, a helpful personal AI coding assistant. "
                    "Help the user write, understand and debug code. "
                    "Give practical and clear answers."
                )
            },
            {
                "role": "user",
                "content": request.message
            }
        ]
    }

    try:

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=data,
            timeout=90
        )

        # Try to read OpenRouter's response
        try:
            result = response.json()
        except ValueError:
            result = {
                "raw_response": response.text
            }

        # OpenRouter returned an HTTP error
        if response.status_code >= 400:

            return {
                "success": False,
                "status_code": response.status_code,
                "error": result.get(
                    "error",
                    result.get(
                        "message",
                        result.get("raw_response", "OpenRouter request failed.")
                    )
                )
            }

        # Successful response
        choices = result.get("choices", [])

        if not choices:
            return {
                "success": False,
                "error": "OpenRouter returned no choices.",
                "details": result
            }

        message = choices[0].get("message", {})

        answer = message.get("content")

        if not answer:
            return {
                "success": False,
                "error": "OpenRouter returned an empty answer.",
                "details": result
            }

        return {
            "success": True,
            "answer": answer
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": "OpenRouter request timed out."
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "error": f"Network error: {str(error)}"
        }

    except Exception as error:

        return {
            "success": False,
            "error": f"Server error: {str(error)}"
        }
