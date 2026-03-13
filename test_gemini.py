import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "AIzaSyBSa7aibZiDkhTXFpK3NOxD7ESVjR4runw":
    print("API Key not set properly.")
else:
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="Hello! Are you there?"
        )
        print("Response received:", response.text)
    except Exception as e:
        print("Error:", str(e))
