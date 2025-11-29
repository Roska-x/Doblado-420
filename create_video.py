import json
from moviepy import ImageSequenceClip, AudioFileClip
import os

def create_avatar_video(lip_sync_file, audio_file, output_video='avatar_video.mp4', fps=24):
    with open(lip_sync_file, 'r') as f:
        lip_sync_data = json.load(f)

    frames = []
    prev_time = 0
    for item in lip_sync_data:
        time = item['time']
        mouth = item['mouth']
        duration = time - prev_time
        if duration > 0:
            frame_path = f'avatar_frames/avatar_{mouth}.png'
            if os.path.exists(frame_path):
                num_frames = max(1, int(duration * fps))
                frames.extend([frame_path] * num_frames)
        prev_time = time

    # Crear clip de secuencia de imágenes
    if frames:
        clip = ImageSequenceClip(frames, fps=fps)
        # Agregar audio
        if os.path.exists(audio_file):
            audio = AudioFileClip(audio_file)
            if audio.duration > clip.duration:
                audio = audio.subclipped(0, clip.duration)
            clip = clip.with_audio(audio)
        # Renderizar
        clip.write_videofile(output_video, codec="libx264", audio_codec="aac", logger=None)
        print(f"Video creado: {output_video}, duración: {clip.duration}s")
    else:
        print("No frames to create video")

if __name__ == "__main__":
    create_avatar_video('lip_sync_test.json', 'temp_audio_es.mp3', 'avatar_test.mp4')