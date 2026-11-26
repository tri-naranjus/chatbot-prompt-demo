# Prueba tu chatbot

Demo web protegida para conversar con el prompt guardado en OpenAI, mediante Responses API.

## Despliegue en Vercel

1. Entra en Vercel y elige **Add New → Project**.
2. Importa el repositorio `tri-naranjus/chatbot-prompt-demo`.
3. Antes de desplegar, añade estas variables privadas en **Environment Variables**:
   - `OPENAI_API_KEY`: la clave de API de OpenAI.
   - `DEMO_PASSWORD`: una contraseña para compartir solo con quienes vayan a probar la demo.
4. Pulsa **Deploy**. Vercel detecta la aplicación FastAPI desde `app.py` y publica la web.
5. Comparte la URL de producción y la contraseña de demo con tus probadores.

Si añades o cambias una variable después del primer despliegue, vuelve a desplegar el proyecto. La clave de API no debe aparecer en GitHub, en el navegador ni en el chat. La contraseña de demo es distinta de la clave de API.

## Prueba local opcional (Windows, PowerShell)

```powershell
git clone https://github.com/tri-naranjus/chatbot-prompt-demo.git
cd chatbot-prompt-demo
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:OPENAI_API_KEY = "tu-clave-de-api"
$env:DEMO_PASSWORD = "tu-clave-privada-de-demo"
uvicorn app:app --reload
```

Abre http://127.0.0.1:8000.

## Cómo funciona

El navegador envía el mensaje a `/api/chat`, que exige la contraseña de demo y llama a `client.responses.create` con el prompt `pmpt_6b07deb3635c8193a92a4a2ddc30340806061fd9ec1527fa`, versión `1`. El navegador conserva el ID de respuesta anterior para mantener el hilo. La clave de OpenAI se lee solo desde el entorno del backend.

La demo es para un grupo controlado: la contraseña se comparte con los probadores, así que configura una contraseña única y vigila el consumo del proyecto de API.
