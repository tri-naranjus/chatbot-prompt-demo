import os
import time
from collections import defaultdict, deque
from typing import Deque

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, Field

PROMPT_ID = "pmpt_6b07deb3635c8193a92a4a2ddc30340806061fd9ec1527fa"
PROMPT_VERSION = "1"
MAX_MESSAGE_LENGTH = 6000
RATE_LIMIT = 20
RATE_WINDOW_SECONDS = 60

client = OpenAI()  # Lee OPENAI_API_KEY del entorno
app = FastAPI(title="Chatbot prompt demo")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Demo local: conserva el response_id mientras el proceso siga activo.
previous_responses: dict[str, str] = {}
requests_by_session: dict[str, Deque[float]] = defaultdict(deque)


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=16, max_length=100)
    message: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/chat")
def chat(body: ChatRequest, request: Request):
    now = time.time()
    timestamps = requests_by_session[body.session_id]
    while timestamps and now - timestamps[0] > RATE_WINDOW_SECONDS:
        timestamps.popleft()
    if len(timestamps) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Has enviado demasiados mensajes. Espera un minuto.")
    timestamps.append(now)

    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Escribe un mensaje antes de enviarlo.")

    try:
        params = {
            "prompt": {"id": PROMPT_ID, "version": PROMPT_VERSION},
            "input": message,
        }
        previous_id = previous_responses.get(body.session_id)
        if previous_id:
            params["previous_response_id"] = previous_id

        response = client.responses.create(**params)
        previous_responses[body.session_id] = response.id
        return {"reply": response.output_text, "response_id": response.id}
    except Exception as exc:
        # No devolvemos detalles internos ni credenciales al navegador.
        raise HTTPException(status_code=502, detail="No se pudo completar la respuesta. Revisa la clave y el acceso a la API.") from exc
