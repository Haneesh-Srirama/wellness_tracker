import os
import streamlit as st
from google import genai

def get_gemini_response(prompt_or_part, context_df, history=None):
    """Query Gemini with the user's context, history, and either a string prompt or an Audio Part."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
    
    if not api_key:
        return "Gemini API Key is missing. Please set GEMINI_API_KEY in your .env file or Streamlit settings."

    try:
        # Initialize Gemini Client
        client = genai.Client(api_key=api_key)
        
        # Build context string
        if context_df.empty:
            context_str = "No health data recorded yet."
        else:
            context_str = context_df.tail(7).to_string(index=False) 

        system_prompt = (
            f"You are a helpful wellness assistant. You have access to the user's recent health data:\n\n"
            f"{context_str}\n\n"
            f"Please answer the user's question based on this data. Be concise, encouraging, and clear. Do not offer medical advice."
        )
        
        # Determine history if any
        formatted_history = []
        if history:
            for msg in history:
                role = 'user' if msg['role'] == 'user' else 'model'
                # Avoid passing the very last message since that's our current prompt
                formatted_history.append({"role": role, "parts": [{"text": msg['content']}]})
                
            # Pop the last element (which is the current prompt) if it matches our text prompt
            if isinstance(prompt_or_part, str):
                if formatted_history and formatted_history[-1]['role'] == 'user' and formatted_history[-1]['parts'][0]['text'] == prompt_or_part:
                    formatted_history.pop()

        chat = client.chats.create(
            model='gemini-2.5-flash',
            config=dict(
                system_instruction=system_prompt,
                temperature=0.7
            ),
            history=formatted_history if formatted_history else None
        )
        
        # If the input is a complex Part (like WebM Audio), pass it as a list
        if isinstance(prompt_or_part, str):
            payload = prompt_or_part
        else:
            # Tell the AI to transcribe and respond to the attached audio
            payload = [prompt_or_part, "Please transcribe and respond to my voice message in the context of my health data."]

        response = chat.send_message(payload)
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return (
                "⚠️ **API Quota Exceeded!**\n\n"
                "You have hit the free-tier rate limit for the Google Gemini API (15 Requests / Minute or 1500 / Day). "
                "Please wait a few moments before sending another message, or upgrade your Google AI Studio billing plan."
            )
        return f"Error communicating with Gemini: {error_msg}"
