import re
import os
import requests

def parse_srt(file_path):
    """Parse SRT file and return a list of text segments."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by double newlines to get each subtitle block
    blocks = content.strip().split('\n\n')
    texts = []
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            # Skip the index and timestamp, take the text
            text = ' '.join(lines[2:]).strip()
            texts.append(text)
    return texts

def generate_report(texts):
    """Generate a structured report from the transcript texts using Grok AI."""
    # Concatenate all texts
    full_text = ' '.join(texts)

    # Configure OpenRouter
    api_key = os.getenv('OPEN_ROUTE_API')
    if api_key:
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
                    "content": f"""
                    Basado en el siguiente transcripto de un video sobre cannabis, genera un informe estructurado en formato Markdown orientado al cultivo profesional de cannabis.
                    Organiza la información en secciones lógicas con títulos y subtítulos claros, enfocándote en aspectos relevantes para el cultivo profesional como morfología, origen, historia, usos, consejos de cultivo, variedades, técnicas de siembra, manejo de plagas, cosecha, etc.
                    Incluye un resumen al inicio.
                    Expande la información con conocimientos adicionales verificados y actualizados sobre el cultivo de cannabis, corroborando y completando los datos del transcripto con información experta confiable.
                    Asegúrate de que el informe sea coherente, bien estructurado, preciso, informativo y capture los puntos clave del contenido, siempre orientado al cultivo profesional de cannabis con todos los conocimientos disponibles.
                    Transcripto: {full_text}
                    """
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            report = result['choices'][0]['message']['content']
        except Exception as e:
            report = f"Error generando informe con IA: {str(e)}. Usando lógica básica.\n\n# Informe sobre Cannabis\n\n## Resumen\n\nResumen del contenido del video sobre cannabis.\n\n## Contenido Completo\n\n{full_text}"
    else:
        # Fallback to basic logic if no API key
        report = f"# Informe sobre Cannabis\n\n## Resumen\n\nResumen del contenido del video sobre cannabis.\n\n## Contenido Completo\n\n{full_text}"

    return report

if __name__ == "__main__":
    srt_file = "Sprays For Odor Control In Cannabis Production - español.srt"
    texts = parse_srt(srt_file)
    report = generate_report(texts)

    with open("informe_sprays_cannabis.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("Informe generado: informe_sprays_cannabis.md")