from modules.chatbot import get_gemini_response

def send_voice_query_to_gemini(prompt, df, messages):
    """
    Acts as the integration layer for voice-transcribed text to the Gemini API.
    Calls the underlying chatbot module to maintain unified logic.
    """
    return get_gemini_response(prompt, df, messages)
