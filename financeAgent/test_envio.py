"""Script de prueba: envía un mensaje de WhatsApp a tu número.
Correr desde la raíz: python financeAgent/test_envio.py
"""
import asyncio
import sys
from pathlib import Path

# Agregamos la raíz al path para poder importar shared/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.messaging.whatsapp_client import WhatsAppClient
from financeAgent.config import settings

# IMPORTANTE: cambiá esto por tu número, en formato internacional SIN el "+"
# Colombia ejemplo: 573001234567 (57 = código país)
# México ejemplo:   521555... 
# Argentina:        549...
MI_NUMERO = "573222139371"  # ← cambiá esto

async def main():
    cliente = WhatsAppClient(
        access_token=settings.whatsapp_access_token,
        phone_number_id=settings.whatsapp_phone_number_id
    )
    
    print(f"Enviando mensaje a {MI_NUMERO}...")
    try:
        resultado = await cliente.enviar_texto(
            MI_NUMERO, 
            "Hola desde mi Finance Agent 👋 Si ves esto, las credenciales están bien."
        )
        print("✅ Enviado correctamente")
        print(f"Respuesta de Meta: {resultado}")
    except Exception as e:
        print(f"❌ Error al enviar: {e}")
        # Imprimir más detalles si es un error HTTP
        if hasattr(e, "response"):
            print(f"Detalle: {e.response.text}")

if __name__ == "__main__":
    asyncio.run(main())