import streamlit as st
from database.crud import get_user_data_df
from modules.voice_assistant import handle_audio_recording, extract_audio_bytes, transcribe_audio_with_groq
from modules.chatbot_integration import send_voice_query_to_gemini

# Ensure the user is logged in via session state
if 'username' not in st.session_state or not st.session_state.username:
    st.warning("Please log in from the main page first.")
    st.stop()

username = st.session_state.username

def inject_chat_css():
    st.markdown("""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        /* Apply Font */
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .block-container {
            animation: fadeIn 0.8s ease-out;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Headers styling */
        h1, h2, h3 {
            color: #E0E0E0 !important;
            font-weight: 700 !important;
        }
        
        h1 {
            background: -webkit-linear-gradient(45deg, #FF6B6B, #FFE66D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #0F0F1A;
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        
        /* Chat UI styling */
        .stChatMessage {
            background-color: rgba(30, 30, 46, 0.6) !important;
            border-radius: 12px;
            padding: 10px 15px;
            margin-bottom: 10px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .stChatInput {
            border-radius: 20px !important;
        }
        </style>
    """, unsafe_allow_html=True)

inject_chat_css()

st.title("💬 Your AI Health Assistant")
st.write("Ask questions about your health tracking data via text or voice and get personalized insights from AI.")

df = get_user_data_df(username)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Voice & Text Input Section ---
prompt = None

# Handle Mic Recording modularly
audio = handle_audio_recording()

# Use traditional chat input
text_prompt = st.chat_input("E.g., I feel weak today. Is there an issue in my tracking?")

audio_bytes = None
transcribed_text = None

if audio:
    audio_bytes = extract_audio_bytes(audio)
    if audio_bytes:
        with st.spinner("Transcribing your voice with Groq..."):
            transcribed_text = transcribe_audio_with_groq(audio_bytes)

# Logic to determine if we got prompt from text or voice
if text_prompt:
    prompt = text_prompt
elif transcribed_text:
    prompt = transcribed_text
else:
    prompt = None

# Process the prompt (either text or voice transcription)
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your data..."):
            response = send_voice_query_to_gemini(prompt, df, st.session_state.messages)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
