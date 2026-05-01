import json
from google import genai
from google.genai import types

class GeminiClient:
    """Cliente reutilizable para Gemini. 
    
    Cada agente lo instancia con sus propias credenciales.
    """
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model = model
        self.client = genai.Client(api_key=api_key)

    async def generar_json(self, texto: str, system_prompt: str, temperatura: float = 0.2) -> dict:
        """Genera respuesta forzada a JSON estructurado."""

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=texto,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperatura,
                response_mime_type="application/json",
            ),
        )
        return json.loads(response.text)
    
    async def generar_texto(self, prompt: str, temperatura: float = 0.2) -> str:
        """Genera respuesta de texto."""
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=temperatura),
        )
        return response.text.strip()