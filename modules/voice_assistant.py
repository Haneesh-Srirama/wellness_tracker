import os
import io
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from groq import Groq

def handle_audio_recording():
    """Renders the microphone component and captures audio."""
    mic_container = st.container()
    with mic_container:
        col1, col2 = st.columns([8, 1])
        with col2:
            audio = mic_recorder(
                start_prompt="🎙️ Voice",
                stop_prompt="Listening...",
                just_once=True,
                use_container_width=True,
                key='mic'
            )
    return audio

def extract_audio_bytes(audio_dict):
    """Returns the raw audio bytes (WebM format from browser)."""
    if not audio_dict or 'bytes' not in audio_dict:
        return None
    return audio_dict['bytes']

def transcribe_audio_with_groq(audio_bytes):
    """Transcribes audio bytes to text using Groq's ultra-fast Whisper model."""
    if not audio_bytes:
        return None
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            try:
                api_key = st.secrets["GROQ_API_KEY"]
            except Exception:
                pass
            
        if not api_key:
            st.error("Groq API key not found. Please add GROQ_API_KEY to your .env file.")
            return None
            
        client = Groq(api_key=api_key)
        
        # Groq expects a tuple (filename, file_like_object)
        file_tuple = ("audio.webm", io.BytesIO(audio_bytes))
        
        transcription = client.audio.transcriptions.create(
          file=file_tuple,
          model="whisper-large-v3-turbo",
          response_format="json",
          language="en"
        )
        return transcription.text
    except Exception as e:
        st.error(f"Error transcribing audio with Groq: {e}")
        return None
