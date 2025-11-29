from phonemizer import phonemize
import re
import json

# Mapeo simple de fonemas IPA a formas de boca (A-H, X)
phoneme_to_mouth = {
    'a': 'A', 'ɑ': 'A', 'æ': 'A', 'ʌ': 'A', 'ə': 'A', 'ɐ': 'A',
    'e': 'E', 'ɛ': 'E', 'ɪ': 'E', 'i': 'E',
    'o': 'O', 'ɔ': 'O', 'ʊ': 'O', 'u': 'O',
    'p': 'B', 'b': 'B', 'm': 'B',
    'f': 'F', 'v': 'F',
    'θ': 'D', 'ð': 'D',
    't': 'C', 'd': 'C', 'n': 'C', 'l': 'C', 'r': 'C',
    'ʃ': 'C', 'ʒ': 'C', 's': 'C', 'z': 'C',
    'k': 'G', 'g': 'G', 'ŋ': 'G',
    'h': 'H',
    'w': 'H', 'j': 'H',
    ' ': 'X',  # pausa
}

def text_to_phonemes(text, language='es'):
    # Fonemizar el texto
    phonemes = phonemize(text, language=language, backend='espeak', strip=True, preserve_punctuation=False)
    return phonemes

def phonemes_to_mouth_shapes(phonemes):
    shapes = []
    for ph in phonemes:
        if ph in phoneme_to_mouth:
            shapes.append(phoneme_to_mouth[ph])
        else:
            shapes.append('X')  # default
    return shapes

def generate_lip_sync_data(segments, output_file='lip_sync.json'):
    lip_sync_data = []
    for seg in segments:
        start = seg['start']
        end = seg['end']
        text = seg['text']
        phonemes = text_to_phonemes(text)
        shapes = phonemes_to_mouth_shapes(phonemes)
        duration = end - start
        num_phonemes = len(shapes)
        if num_phonemes > 0:
            time_per_phoneme = duration / num_phonemes
            current_time = start
            for shape in shapes:
                lip_sync_data.append({
                    'time': current_time,
                    'mouth': shape
                })
                current_time += time_per_phoneme
    with open(output_file, 'w') as f:
        json.dump(lip_sync_data, f, indent=2)
    return lip_sync_data

if __name__ == "__main__":
    # Ejemplo con segmentos de prueba
    test_segments = [
        {'start': 0, 'end': 2, 'text': 'Hola mundo'},
        {'start': 2, 'end': 4, 'text': 'Esto es una prueba'}
    ]
    data = generate_lip_sync_data(test_segments, 'lip_sync_test.json')
    print("Datos de lip-sync generados:", data[:10])  # primeros 10