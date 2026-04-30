"""Cliente reutilizable para Whatsapp API.

Es una clase genériica: cualquier agente que necesite Whatsapp la importa
y la instancia con sus propias credenciales.

Uso: 
    cliente: WhatsAppClient(access_token="---", phone_number_id="---")
    await cliente.enviar_texto(to="3121234567", texto="Hola, ¿cómo estás?")
"""

from codecs import strict_errors
import httpx

class WhatsAppClient:
    
    def __init__(self, access_token: str, phone_number_id: str):
        """
        Args_ 
            access_token: token de acceso de Meta (Bearer token)
            phone_number_id: ID del número de WhatsApp emisor (no es el número en sí)
        """

        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.url = f"https://graph.facebook.com/v21.0/{phone_number_id}/messages"
    
    async def enviar_texto(self, to: str, texto: str):
        """Envía un mensaje de texto a un número de WhatsApp.
        
        
        Args:
            to: número de WhatsApp destinatario (sin '+', ej: "573121234567")
            texto: contenido del mensaje (máx 4096 caracteres)

        Returns: 
            dict con la respuesta de Meta (id del mensaje, estado, etc)
        
        Raises: 
            httpx.HTTPStatusError: si Meta rechaza el envío.
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": texto,
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def marcar_leido(self, message_id: str) -> None:
        """Marca un mensaje como leído.
        Args:
            message_id: ID del mensaje recibido (campo 'id' del webhook).
        """

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(self.url, headers=headers, json=payload)
        
    @staticmethod
    def parsear_webhook(data: dict) -> dict | None:
        try:
            value = data["entry"][0]["changes"][0]["value"]
            if "messages" not in value:
                return None
                
            msg = value["messages"][0]
            contact = value.get("contacts", [{}])[0]
            return {
                "message_id": msg["id"],
                "from_number": msg["from"],
                "nombre": contact.get("profile", {}).get("name", "Usuario"),
                "tipo": msg["type"],
                "texto": msg.get("text", {}).get("body", ""),
                "timestamp": msg["timestamp"]
            }
        except (KeyError, IndexError):
            return None