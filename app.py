import hmac
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from openai import OpenAI
from pydantic import BaseModel, Field

PROMPT_ID = "pmpt_6b07deb3635c8193a92a4a2ddc30340806061fd9ec1527fa"
PROMPT_VERSION = "1"
MAX_MESSAGE_LENGTH = 6000

app = FastAPI(title="Chatbot prompt demo")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)
    previous_response_id: str | None = Field(default=None, max_length=200)


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/chat")
def chat(body: ChatRequest, request: Request):
    api_key = os.getenv("OPENAI_API_KEY")
    access_password = os.getenv("DEMO_PASSWORD")
    if not api_key or not access_password:
        raise HTTPException(status_code=503, detail="La demo todavía no está configurada en Vercel.")

    supplied_password = request.headers.get("x-demo-password", "")
    if not hmac.compare_digest(supplied_password, access_password):
        raise HTTPException(status_code=401, detail="Contraseña de demo incorrecta.")

    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Escribe un mensaje antes de enviarlo.")

    try:
        client = OpenAI(api_key=api_key)
        params = {
            "prompt": {"id": PROMPT_ID, "version": PROMPT_VERSION},
            "input": message,
        }
        if body.previous_response_id:
            params["previous_response_id"] = body.previous_response_id
        response = client.responses.create(**params)
        return {"reply": response.output_text, "response_id": response.id}
    except Exception as exc:
        raise HTTPException(status_code=502, detail="No se pudo completar la respuesta con OpenAI.") from exc
