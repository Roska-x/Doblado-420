from PIL import Image, ImageDraw
import os

def create_base_avatar():
    # Intentar cargar la imagen del usuario
    try:
        img = Image.open('avatar/avatar.jpeg').convert('RGB')
        # Mantener resolución alta, redimensionar manteniendo aspecto
        img.thumbnail((800, 800), Image.Resampling.LANCZOS)
        print(f"Usando imagen personalizada del avatar, tamaño: {img.size}")
    except Exception as e:
        print(f"No se pudo cargar avatar personalizado: {e}. Usando avatar simple.")
        # Crear imagen base del avatar (cara simple)
        img = Image.new('RGB', (400, 400), color='lightblue')
        draw = ImageDraw.Draw(img)

        # Cabeza
        draw.ellipse((100, 100, 300, 300), fill='peachpuff')

        # Ojos
        draw.ellipse((140, 140, 180, 180), fill='white')
        draw.ellipse((220, 140, 260, 180), fill='white')
        draw.ellipse((150, 150, 170, 170), fill='black')
        draw.ellipse((230, 150, 250, 170), fill='black')

        # Nariz
        draw.polygon([(200, 180), (190, 220), (210, 220)], fill='peachpuff')

    return img

def create_mouth_shape(base_img, mouth_type):
    img = base_img.copy()
    draw = ImageDraw.Draw(img)

    width, height = img.size
    scale_x = width / 200
    scale_y = height / 200

    # Posición de la boca escalada
    mouth_y = int(120 * scale_y)
    mouth_left = int(85 * scale_x)
    mouth_right = int(115 * scale_x)

    if mouth_type == 'A':  # Ah
        draw.ellipse((mouth_left, mouth_y, mouth_right, mouth_y + int(20 * scale_y)), fill='black')
    elif mouth_type == 'B':  # B
        draw.ellipse((int(90 * scale_x), mouth_y, int(110 * scale_x), mouth_y + int(15 * scale_y)), fill='black')
    elif mouth_type == 'C':  # Ch
        draw.rectangle((mouth_left, mouth_y, mouth_right, mouth_y + int(10 * scale_y)), fill='black')
    elif mouth_type == 'D':  # D
        draw.ellipse((mouth_left, mouth_y, mouth_right, mouth_y + int(15 * scale_y)), fill='black')
    elif mouth_type == 'E':  # Eh
        draw.ellipse((mouth_left, mouth_y, mouth_right, mouth_y + int(10 * scale_y)), fill='black')
    elif mouth_type == 'F':  # F
        draw.rectangle((int(90 * scale_x), mouth_y, int(110 * scale_x), mouth_y + int(5 * scale_y)), fill='black')
    elif mouth_type == 'G':  # G
        draw.ellipse((mouth_left, mouth_y, mouth_right, mouth_y + int(12 * scale_y)), fill='black')
    elif mouth_type == 'H':  # H
        draw.ellipse((mouth_left, mouth_y, mouth_right, mouth_y + int(8 * scale_y)), fill='black')
    elif mouth_type == 'X':  # Rest
        draw.line((mouth_left, mouth_y + int(5 * scale_y), mouth_right, mouth_y + int(5 * scale_y)), fill='black', width=max(1, int(3 * scale_x)))

    return img

if __name__ == "__main__":
    base = create_base_avatar()
    os.makedirs('avatar_frames', exist_ok=True)

    phonemes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'X']
    for phoneme in phonemes:
        mouth_img = create_mouth_shape(base, phoneme)
        mouth_img.save(f'avatar_frames/avatar_{phoneme}.png')
        print(f'Creado avatar_{phoneme}.png')

    print("Avatares creados en avatar_frames/")