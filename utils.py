import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key: str = os.environ["GEMINI_API_KEY"]

def get_gemini_model(model: str):
    return genai.GenerativeModel(model)

def generate_content(prompt: str):
    genai.configure(api_key= gemini_api_key)
    model = get_gemini_model("gemini-1.5-flash")
    return model.generate_content(prompt)
