import streamlit as st
import os
import asyncio
import edge_tts
from moviepy import VideoFileClip, AudioFileClip
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator, DeeplTranslator
from datetime import timedelta
import requests
from fpdf import FPDF
from generate_lip_sync import generate_lip_sync_data
from create_video import create_avatar_video

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="AI Video Dubber Pro", page_icon="🎬", layout="centered")

# --- ESTILOS CSS MINIMALISTAS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold;}
    .reportview-container { margin-top: -2em; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES CORE ---

@st.cache_resource
def load_whisper():
    # Usamos 'tiny' o 'base' para velocidad extrema. Usa 'medium' para mayor precisión.
    # int8 para que vuele en CPU si no tienes GPU.
    return WhisperModel("base", device="cpu", compute_type="int8")

def format_timestamp(seconds):
    td = timedelta(seconds=seconds)
    # Formato simple para SRT: HH:MM:SS,mmm
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

async def generate_voice_over(text_segments, output_audio_path):
    # Voz neuronal de Microsoft (Español Argentino)
    VOICE = "es-AR-TomasNeural" # Opciones: es-MX-DaliaNeural, es-ES-AlvaroNeural

    full_text = " ".join([seg['text'] for seg in text_segments])
    communicate = edge_tts.Communicate(full_text, VOICE)
    await communicate.save(output_audio_path)

def create_srt(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            start = format_timestamp(seg['start'])
            end = format_timestamp(seg['end'])
            text = seg['text']
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

def post_process_text(text):
    # Diccionario de reemplazos para hacer la traducción más natural en español argentino
    # y ajustar términos específicos de cannabis, química y cultivo
    replacements = {
        "capullo": "cogollo",  # buds en cannabis
        "simuladores": "milímetros",  # corrección de traducción errónea
        "Es posible que": "Puede que",  # más natural
        "en esta videoconferencia": "en esta charla",  # más coloquial
        "Universidade Debaco": "Universidad Debaco",  # corrección si hay errores
        # Agregar más según sea necesario
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def generate_report(texts):
    """Generate a structured report from the transcript texts using OpenRoute AI."""
    # Concatenate all texts
    full_text = ' '.join(texts)

    # Configure OpenRoute
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
                    Basado en el siguiente transcripto de un video, genera un informe estructurado en formato Markdown.
                    Organiza la información en secciones lógicas con títulos y subtítulos claros.
                    Incluye un resumen al inicio.
                    Asegúrate de que el informe sea coherente, bien estructurado y capture los puntos clave del contenido.
                    Transcripto: {full_text}
                    """
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            report = result['choices'][0]['message']['content']
        except Exception as e:
            report = f"Error generando informe con IA: {str(e)}. Usando lógica básica.\n\n# Informe\n\n{full_text}"
    else:
        # Fallback to basic logic if no API key
        report = f"# Informe del Video\n\n## Resumen\n\nResumen del contenido del video.\n\n## Contenido Completo\n\n{full_text}"

    return report

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    lines = text.split('\n')
    for line in lines:
        if line.startswith('# '):
            pdf.set_font("Arial", 'B', 16)
            pdf.multi_cell(0, 10, line[2:])
            pdf.set_font("Arial", size=12)
        elif line.startswith('## '):
            pdf.set_font("Arial", 'B', 14)
            pdf.multi_cell(0, 10, line[3:])
            pdf.set_font("Arial", size=12)
        elif line.strip() == '':
            pdf.ln(10)
        else:
            pdf.multi_cell(0, 10, line)
    return pdf.output(dest='S')

def generate_json(original_segments, translated_segments, report_md, srt_content, video_name):
    """Generate structured JSON from video data using Grok for professional expansion."""
    import json
    from datetime import datetime

    # Prepare data for Grok
    data_summary = {
        "video_name": video_name,
        "processing_timestamp": datetime.now().isoformat(),
        "original_transcript": [{"start": seg.start, "end": seg.end, "text": seg.text} for seg in original_segments],
        "translated_transcript": translated_segments,
        "srt_content": srt_content,
        "report_markdown": report_md
    }

    # Use Grok to structure and expand
    api_key = os.getenv('OPEN_ROUTE_API')
    if api_key:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        prompt = f"""
        Based on the following video processing data, generate a professional, structured JSON object optimized for LLM consumption.
        Expand the information where appropriate with additional context, key topics, entities, and structured summaries.
        Include sections for metadata, transcripts, analysis, and expanded insights.

        Data: {json.dumps(data_summary, ensure_ascii=False)}

        Return only valid JSON without any markdown formatting or explanations.
        """
        data = {
            "model": "x-ai/grok-4.1-fast:free",
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            json_str = result['choices'][0]['message']['content'].strip()
            # Remove any potential markdown code blocks
            if json_str.startswith('```json'):
                json_str = json_str[7:]
            if json_str.endswith('```'):
                json_str = json_str[:-3]
            json_data = json.loads(json_str)
        except Exception as e:
            # Fallback to basic JSON structure
            json_data = {
                "error": f"Failed to generate enhanced JSON with AI: {str(e)}",
                "fallback_data": data_summary
            }
    else:
        # Fallback without API
        json_data = {
            "metadata": {
                "video_name": video_name,
                "processing_timestamp": datetime.now().isoformat(),
                "source": "AI Video Dubber"
            },
            "transcripts": {
                "original": data_summary["original_transcript"],
                "translated": translated_segments
            },
            "subtitles": srt_content,
            "report": report_md,
            "note": "Enhanced structuring requires OPEN_ROUTE_API key"
        }

    return json.dumps(json_data, ensure_ascii=False, indent=2)

def ask_chatbot(question, full_report):
    """Ask questions about the full report using the same AI model."""
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
                    Basado en el siguiente informe completo, responde a la pregunta del usuario de manera clara, concisa y precisa.
                    Si la pregunta no está relacionada con el contenido del informe, indica que no puedes responder sobre temas fuera del informe.

                    Informe completo:
                    {full_report}

                    Pregunta: {question}
                    """
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            answer = result['choices'][0]['message']['content']
        except Exception as e:
            answer = f"Error consultando al chatbot: {str(e)}. Intenta de nuevo."
    else:
        answer = "No se puede acceder al chatbot porque falta la clave API de OpenRoute."

    return answer

# --- INTERFAZ DE USUARIO ---

st.title("🎬 Doblado 420")
st.markdown("Traduce videos de **Inglés 🇺🇸** a **Español Argentino 🇦🇷** con IA. Rápido y sin coste.")

deepl_api_key = st.text_input("API Key de DeepL (opcional para traducciones más naturales)", type="password")

uploaded_files = st.file_uploader("Sube tus videos (MP4, MKV, MOV)", type=["mp4", "mkv", "mov"], accept_multiple_files=True)

generate_avatar = st.checkbox("🎭 Generar video de avatar animado (experimental)")

if uploaded_files:
    if st.button("🚀 INICIAR MAGIA (Traducir & Doblar Todos)"):
        total = len(uploaded_files)
        progress_bar = st.progress(0)
        status_text = st.empty()
        st.session_state.results = []
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Procesando video {i+1}/{total}: {uploaded_file.name}")
            original_name = uploaded_file.name
            name_without_ext = os.path.splitext(original_name)[0]
            dubbed_video_name = f"{name_without_ext} - español.mp4"
            dubbed_srt_name = f"{name_without_ext} - español.srt"
            dubbed_report_name = f"{name_without_ext} - informe.md"
            temp_video_path = f"temp_video_{i}.mp4"
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            try:
                # 1. Transcripción
                model = load_whisper()
                segments_gen, _ = model.transcribe(temp_video_path, language="en")
                segments = list(segments_gen)
                # 2. Traducción
                if deepl_api_key:
                    translator = DeeplTranslator(api_key=deepl_api_key, source='en', target='es')
                else:
                    translator = GoogleTranslator(source='en', target='es')
                translated_segments = []
                for seg in segments:
                    try:
                        translated_text = translator.translate(seg.text)
                    except Exception as e:
                        # Try alternative translator
                        if isinstance(translator, DeeplTranslator):
                            alt_translator = GoogleTranslator(source='en', target='es')
                        else:
                            alt_translator = DeeplTranslator(api_key=deepl_api_key, source='en', target='es') if deepl_api_key else GoogleTranslator(source='en', target='es')
                        try:
                            translated_text = alt_translator.translate(seg.text)
                        except Exception as e2:
                            # If both fail, use original text
                            translated_text = seg.text
                    translated_text = post_process_text(translated_text)
                    translated_segments.append({
                        "start": seg.start,
                        "end": seg.end,
                        "text": translated_text
                    })
                # 3. Generar Subtítulos
                srt_path = dubbed_srt_name
                create_srt(translated_segments, srt_path)
                # 4. Generar Audio
                audio_output_path = f"temp_audio_es_{i}.mp3"
                asyncio.run(generate_voice_over(translated_segments, audio_output_path))
                # 5. Generar Avatar (opcional)
                avatar_path = None
                if generate_avatar:
                    lip_sync_file = f'lip_sync_{i}.json'
                    generate_lip_sync_data(translated_segments, lip_sync_file)
                    avatar_video_name = f"{name_without_ext} - avatar.mp4"
                    create_avatar_video(lip_sync_file, audio_output_path, avatar_video_name)
                    avatar_path = avatar_video_name
                # 6. Mezclar
                video_clip = VideoFileClip(temp_video_path)
                new_audio = AudioFileClip(audio_output_path)
                if new_audio.duration > video_clip.duration:
                    new_audio = new_audio.subclipped(0, video_clip.duration)
                final_clip = video_clip.with_audio(new_audio)
                final_output_path = dubbed_video_name
                final_clip.write_videofile(final_output_path, codec="libx264", audio_codec="aac", logger=None)
                video_clip.close()
                new_audio.close()
                # Generate report
                texts = [seg['text'] for seg in translated_segments]
                report_md = generate_report(texts)
                # Generate JSON
                srt_content = open(srt_path, 'r', encoding='utf-8').read()
                json_data = generate_json(segments, translated_segments, report_md, srt_content, original_name)
                json_name = f"{name_without_ext} - data.json"
                # Store result
                result = {
                    'name': original_name,
                    'video_path': final_output_path,
                    'srt_path': srt_path,
                    'report_md': report_md,
                    'report_name': dubbed_report_name,
                    'json_data': json_data,
                    'json_name': json_name,
                    'avatar_path': avatar_path
                }
                st.session_state.results.append(result)
                progress_bar.progress(int((i+1)/total * 100))
            except Exception as e:
                st.error(f"Error procesando {original_name}: {str(e)}")
        status_text.success("✅ ¡Todos los videos procesados!")
        progress_bar.progress(100)

    # Display results
    if 'results' in st.session_state and st.session_state.results:
        st.markdown("### Resultados")
        for result in st.session_state.results:
            st.markdown(f"#### {result['name']}")
            col1, col2 = st.columns(2)
            with col1:
                with open(result['video_path'], "rb") as file:
                    st.download_button(
                        label="⬇️ Descargar Video Doblado",
                        data=file,
                        file_name=os.path.basename(result['video_path']),
                        mime="video/mp4"
                    )
            with col2:
                with open(result['srt_path'], "rb") as file:
                    st.download_button(
                        label="⬇️ Descargar Subtítulos (SRT)",
                        data=file,
                        file_name=os.path.basename(result['srt_path']),
                        mime="text/plain"
                    )
            if result.get('avatar_path'):
                with st.columns(1)[0]:
                    with open(result['avatar_path'], "rb") as file:
                        st.download_button(
                            label="⬇️ Descargar Video de Avatar",
                            data=file,
                            file_name=os.path.basename(result['avatar_path']),
                            mime="video/mp4"
                        )
            report_bytes = result['report_md'].encode('utf-8')
            st.download_button(
                label="⬇️ Descargar Informe (Markdown)",
                data=report_bytes,
                file_name=result['report_name'],
                mime="text/markdown"
            )
            # JSON download
            json_bytes = result['json_data'].encode('utf-8')
            st.download_button(
                label="⬇️ Descargar Datos JSON",
                data=json_bytes,
                file_name=result['json_name'],
                mime="application/json"
            )

        # Combined report
        st.markdown("---")
        combined_report = "# Informe Completo de Todos los Videos\n\n"
        for result in st.session_state.results:
            combined_report += f"## {result['name']}\n\n{result['report_md']}\n\n---\n\n"
        st.markdown(combined_report)
        # Download combined MD
        combined_md_bytes = combined_report.encode('utf-8')
        st.download_button(
            label="⬇️ Descargar Informe Completo (Markdown)",
            data=combined_md_bytes,
            file_name="informe_completo.md",
            mime="text/markdown"
        )
        # Generate PDF
        combined_pdf_bytes = generate_pdf(combined_report)
        st.download_button(
            label="⬇️ Descargar Informe Completo (PDF)",
            data=combined_pdf_bytes,
            file_name="informe_completo.pdf",
            mime="application/pdf"
        )

        # --- CHATBOT SECTION ---
        st.markdown("---")
        st.markdown("### 🤖 Chatbot de Consultas sobre el Informe")
        st.markdown("Haz preguntas sobre el contenido del informe completo generado.")

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f"**Tú:** {msg['content']}")
            else:
                st.markdown(f"**Asistente:** {msg['content']}")

        # Form for input and button
        with st.form(key='chat_form'):
            user_question = st.text_input("Escribe tu pregunta aquí:", key="chat_input")
            submit_button = st.form_submit_button("Preguntar")

        if submit_button and user_question.strip():
            # Add user question to history
            st.session_state.chat_history.append({'role': 'user', 'content': user_question})

            # Get response from chatbot with spinner
            with st.spinner("Pensando..."):
                response = ask_chatbot(user_question, combined_report)

            # Add response to history
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})

            # Rerun to update display
            st.rerun()
