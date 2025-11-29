# 🎬 Doblado 420

Una aplicación web avanzada construida con Streamlit que utiliza inteligencia artificial para traducir videos de inglés a español argentino. Incluye doblaje automático con voz neuronal, generación de subtítulos, informes estructurados y creación opcional de videos de avatar animado.

## ✨ Características Principales

- **Transcripción Automática**: Utiliza Whisper AI para transcribir audio de videos en inglés con alta precisión.
- **Traducción Inteligente**: Traduce el contenido a español argentino usando Google Translate o DeepL (con API key opcional para mejores resultados).
- **Doblaje Neuronal**: Genera voz sintetizada en español argentino utilizando Microsoft Edge TTS.
- **Subtítulos SRT**: Crea archivos de subtítulos sincronizados automáticamente.
- **Videos de Avatar**: Genera videos animados con avatares que sincronizan labios (experimental).
- **Informes IA**: Crea informes estructurados y resúmenes del contenido usando modelos de IA avanzados.
- **Chatbot Interactivo**: Consulta preguntas sobre el contenido de los informes generados usando IA conversacional.
- **Exportación Múltiple**: Descarga videos doblados, subtítulos, informes en Markdown/PDF y datos JSON.
- **Interfaz Web**: Fácil de usar con Streamlit, sin necesidad de conocimientos técnicos avanzados.

## 🛠️ Requisitos del Sistema

- **Python**: 3.8 o superior
- **FFmpeg**: Requerido para el procesamiento de video y audio
- **Espacio en Disco**: Suficiente para videos temporales y procesados
- **Conexión a Internet**: Para traducciones y generación de informes con IA

## 📦 Instalación

1. **Clona el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd ai-video-dubber
   ```

2. **Instala las dependencias**:
   ```bash
   pip install streamlit edge-tts moviepy faster-whisper deep-translator requests fpdf
   ```

3. **Instala FFmpeg** (dependiendo de tu sistema operativo):
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Descarga desde [ffmpeg.org](https://ffmpeg.org/download.html)

## ⚙️ Configuración

1. **Variables de Entorno**:
   Copia el archivo de ejemplo y configura las claves API opcionales:
   ```bash
   cp .env.example .env
   ```

   Edita `.env` con tus claves:
   ```
   OPEN_ROUTE_API=tu_clave_aqui  # Para informes avanzados con IA
   ```

2. **API Keys Opcionales**:
   - **DeepL API Key**: Para traducciones más naturales y precisas
   - **OpenRoute API Key**: Para generación de informes estructurados con IA (usa x-ai/grok)

## 🚀 Uso

1. **Ejecuta la aplicación**:
   ```bash
   streamlit run app.py
   ```

2. **Accede a la interfaz**:
   Abre tu navegador en `http://localhost:8501`

3. **Procesa videos**:
   - Sube uno o varios videos (formatos soportados: MP4, MKV, MOV)
   - Opcionalmente, ingresa tu API key de DeepL
   - Marca la casilla si deseas generar videos de avatar
   - Haz clic en "🚀 INICIAR MAGIA" para procesar

4. **Descarga resultados**:
   - Video doblado en español
   - Archivo de subtítulos SRT
   - Informe en formato Markdown
   - Datos estructurados en JSON
   - Video de avatar (si seleccionado)

5. **Consulta el Chatbot**:
   - Una vez generado el informe completo, puedes hacer preguntas sobre el contenido
   - El chatbot utiliza IA para responder basado en todo el informe generado
   - Presiona Enter o haz clic en "Preguntar" para enviar tu consulta

## 📁 Estructura del Proyecto

```
├── app.py                    # Aplicación principal de Streamlit
├── create_avatar.py          # Generación de avatares animados
├── create_video.py           # Creación de videos con avatares
├── generate_lip_sync.py      # Sincronización de labios
├── generate_avatar_prompts.py # Prompts para avatares
├── generate_report.py        # Generación de informes
├── ai_avatar_help.py         # Utilidades para avatares
├── .env.example              # Ejemplo de variables de entorno
├── .gitignore               # Archivos ignorados por Git
└── README.md                # Este archivo
```

## 🔧 Funcionalidades Técnicas

### Transcripción
- Modelo Whisper "base" optimizado para velocidad
- Soporte para inglés como idioma fuente
- Segmentación automática del audio

### Traducción
- Fallback automático entre Google Translate y DeepL
- Post-procesamiento para español argentino coloquial
- Correcciones específicas para términos técnicos

### Doblaje
- Voz neuronal: "es-AR-TomasNeural" (español argentino)
- Sincronización automática con el video original
- Ajuste de duración para coincidir con el video

### Avatares (Experimental)
- Generación de datos de sincronización labial
- Creación de videos animados con avatares
- Integración con audio doblado

### Informes
- Estructura Markdown profesional
- Resúmenes generados por IA
- Exportación a PDF automática

### Chatbot
- Consultas interactivas sobre el contenido de los informes
- Utiliza el mismo modelo de IA para mantener consistencia
- Historial de conversación persistente durante la sesión
- Respuestas basadas en el informe completo generado

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Áreas de Mejora
- Soporte para más idiomas
- Mejora en la sincronización de labios
- Optimización de rendimiento
- Interfaz más avanzada

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ⚠️ Notas Importantes

- **Experimental**: La función de avatares es experimental y puede requerir ajustes
- **API Keys**: Algunas funcionalidades requieren claves API externas
- **Procesamiento**: Los videos grandes pueden tomar tiempo en procesarse
- **Legal**: Asegúrate de tener derechos para doblar y distribuir los videos procesados

## 🆘 Soporte

Si encuentras problemas:
- Revisa los logs de la aplicación
- Verifica que todas las dependencias estén instaladas
- Asegúrate de que FFmpeg esté correctamente instalado
- Abre un issue en el repositorio con detalles del error

---
No te olvides de dejar tu estrella si te gusto!
**Desarrollado con ❤️ by Roska**
