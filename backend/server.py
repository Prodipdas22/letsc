import os
import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="LETSC AI API")


# Allow the LETSC frontend to communicate with the backend
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
            "error": "OPENROUTER_API_KEY is not configured."
        }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://letsc.example",
        "X-Title": "LETSC Personal AI"
    }

    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are LETSC, a helpful personal AI coding assistant. "
                    "Write clean, understandable and practical code. "
                    "When appropriate, explain the code and identify errors."
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
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        return {
            "answer": answer
        }

    except requests.exceptions.RequestException as error:

        return {
            "error": f"AI request failed: {str(error)}"
        }

    except (KeyError, IndexError):

        return {
            "error": "Unexpected response received from AI provider."
        }
