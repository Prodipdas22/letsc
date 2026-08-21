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


@app.get("/health")
def health():
    return {
        "server": "online",
        "api_key_configured": bool(OPENROUTER_API_KEY)
    }


@app.post("/chat")
def chat(request: ChatRequest):

    if not OPENROUTER_API_KEY:
        return {
            "success": False,
            "error": "OpenRouter API key is NOT configured in Render."
        }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://letscomp.netlify.app",
        "X-Title": "LETSC Personal AI"
    }

    payload = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are LETSC, a personal AI coding assistant. "
                    "Help users write, explain and debug code. "
                    "Give clear and practical answers."
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
            json=payload,
            timeout=90
        )

        print("OpenRouter status:", response.status_code)
        print("OpenRouter response:", response.text)

        try:
            result = response.json()
        except Exception:
            return {
                "success": False,
                "error": "OpenRouter returned non-JSON response.",
                "status_code": response.status_code,
                "raw": response.text[:1000]
            }

        if response.status_code >= 400:

            error_data = result.get("error")

            if isinstance(error_data, dict):
                error_message = error_data.get(
                    "message",
                    "OpenRouter returned an error."
                )
            else:
                error_message = str(
                    error_data or
                    result.get("message") or
                    "OpenRouter request failed."
                )

            return {
                "success": False,
                "error": error_message,
                "status_code": response.status_code
            }

        choices = result.get("choices")

        if not choices:
            return {
                "success": False,
                "error": "OpenRouter returned no choices.",
                "status_code": response.status_code,
                "details": result
            }

        answer = choices[0].get("message", {}).get("content")

        if not answer:
            return {
                "success": False,
                "error": "AI returned an empty response.",
                "details": result
            }

        return {
            "success": True,
            "answer": answer
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": "Request to OpenRouter timed out."
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"Network error: {str(e)}"
        }

    except Exception as e:

        return {
            "success": False,
            "error": f"Unexpected server error: {str(e)}"
        }
