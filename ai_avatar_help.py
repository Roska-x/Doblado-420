import os
import requests
from PIL import Image
import base64
from dotenv import load_dotenv

load_dotenv()

def get_avatar_advice():
    api_key = os.getenv('OPEN_ROUTE_API')
    if not api_key:
        return "No se encontró OPEN_ROUTE_API en .env"

    # Cargar imagen del avatar
    try:
        with open('avatar/avatar.jpeg', 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
    except:
        return "No se pudo cargar la imagen del avatar"

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "x-ai/grok-4.1-fast:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
                        Analiza esta imagen de avatar y dame consejos para mejorarlo para animación de lip-sync en 2D.
                        Sugiere:
                        - Posición ideal de la boca
                        - Mejoras en el diseño para animación
                        - Técnicas de animación más realistas
                        - Alternativas 3D si es apropiado
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error consultando IA: {str(e)}"

if __name__ == "__main__":
    advice = get_avatar_advice()
    print("Consejos de IA para el avatar:")
    print(advice)