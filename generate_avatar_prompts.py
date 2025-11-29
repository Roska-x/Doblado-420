# Prompts para generar imágenes del avatar con diferentes formas de boca para lip-sync
# Usa estos prompts en herramientas de IA como Midjourney, DALL-E, Stable Diffusion, etc.

avatar_base = "Alienígena verde con cabeza calva grande, gafas de sol oscuras, barba rala, camisa blanca holgada, sosteniendo un encendedor naranja y un cigarrillo encendido en la boca, fondo glitch vaporwave cyberpunk, estilo retro-futurista, alta calidad, detallado"

phoneme_prompts = {
    'A': f"{avatar_base}, boca muy abierta en forma de 'A' o 'Ah', mandíbula baja, mostrando dientes si aplica, expresión de sorpresa o vocal larga",
    'B': f"{avatar_base}, boca cerrada con labios juntos en forma de 'B' o 'M', expresión neutra, labio inferior ligeramente protruso",
    'C': f"{avatar_base}, boca en forma de 'Ch' o 'Sh', labios estirados horizontalmente, dientes visibles en línea recta",
    'D': f"{avatar_base}, boca en forma de 'D' o 'Th', lengua tocando dientes superiores, expresión concentrada",
    'E': f"{avatar_base}, boca en forma de 'E' o 'Eh', mandíbula ligeramente abierta, lengua visible en forma de 'E'",
    'F': f"{avatar_base}, boca en forma de 'F' o 'V', dientes superiores mordiendo labio inferior, expresión de 'F'",
    'G': f"{avatar_base}, boca en forma de 'G' o 'K', mandíbula abierta media, fondo de garganta visible",
    'H': f"{avatar_base}, boca en forma de 'H' o vocal abierta, mandíbula relajada, expresión neutral",
    'X': f"{avatar_base}, boca en posición de reposo, labios ligeramente cerrados, expresión relajada, sin movimiento"
}

def generate_prompts():
    print("Prompts para generar imágenes del avatar con formas de boca para lip-sync:")
    print("=" * 80)
    for phoneme, prompt in phoneme_prompts.items():
        print(f"\nPhoneme {phoneme}:")
        print(prompt)
        print("-" * 40)

if __name__ == "__main__":
    generate_prompts()