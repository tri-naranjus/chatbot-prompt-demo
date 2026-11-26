# Prueba tu chatbot

Web mínima para conversar con el prompt guardado en OpenAI, usando Responses API.

## Requisitos

- Python 3.10 o posterior.
- Una clave de API de OpenAI con acceso al proyecto donde está creado el prompt.

## Arranque local en Windows (PowerShell)

Clona el repositorio y entra en la carpeta:

```powershell
git clone https://github.com/tri-naranjus/chatbot-prompt-demo.git
cd chatbot-prompt-demo
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:OPENAI_API_KEY = "tu-clave-de-api"
uvicorn app:app --reload
```

Abre http://127.0.0.1:8000. La clave se lee desde la variable de entorno del proceso Python; no la escribas en `index.html` ni la subas a GitHub.

## macOS o Linux

```bash
git clone https://github.com/tri-naranjus/chatbot-prompt-demo.git
cd chatbot-prompt-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="tu-clave-de-api"
uvicorn app:app --reload
```

## Cómo funciona

El navegador envía el mensaje a `/api/chat`. El backend llama a `client.responses.create` con el prompt `pmpt_6b07deb3635c8193a92a4a2ddc30340806061fd9ec1527fa`, versión `1`, y mantiene la conversación usando el ID de respuesta anterior. La interfaz no muestra la clave de API.

El historial de conversación vive en memoria y se borra al reiniciar el servidor. Este proyecto es una demo local: antes de exponerlo públicamente hay que añadir autenticación y límites de uso adecuados, porque un endpoint público conectado a una clave de API podría generar consumo no autorizado.
