"""Servidor webhook para recibir mensajes entrantes de WhatsApp."""
import asyncio
from fastapi import FastAPI, Request, Response, HTTPException
from shared.messaging.whatsapp_client import WhatsAppClient
from financeAgent.config import settings

app = FastAPI()

cliente = WhatsAppClient(
    access_token=settings.whatsapp_access_token,
    phone_number_id=settings.whatsapp_phone_number_id,
)


@app.get("/webhook")
async def verificar_webhook(request: Request):
    """Meta llama este endpoint UNA vez para confirmar que el servidor es tuyo."""
    params = request.query_params
    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == settings.whatsapp_verify_token
    ):
        return Response(content=params.get("hub.challenge"), media_type="text/plain")
    raise HTTPException(status_code=403, detail="Token inválido")


@app.post("/mensaje")
async def recibir_mensaje(request: Request):
    """Meta envía aquí cada mensaje entrante."""
    data = await request.json()
    mensaje = WhatsAppClient.parsear_webhook(data)

    if mensaje is None:
        return {"status": "ok"}  # notificación de estado, no un mensaje

    print(f"📩 Mensaje de {mensaje['nombre']} ({mensaje['from_number']}): {mensaje['texto']}")

    # Marcar como leído
    await cliente.marcar_leido(mensaje["message_id"])

    # --- ACÁ va tu lógica de agente ---
    respuesta = f"Recibí tu mensaje: {mensaje['texto']}"
    await cliente.enviar_texto(to=mensaje["from_number"], texto=respuesta)

    return {"status": "ok"}