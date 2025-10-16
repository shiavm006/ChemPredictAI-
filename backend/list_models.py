"""
List all available Gemini models
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("No API key found!")
    exit(1)

print(f"✓ API key found: {api_key[:10]}...{api_key[-4:]}\n")

genai.configure(api_key=api_key)

print("Available Gemini Models:")
print("=" * 60)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✓ {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Description: {model.description[:100]}...")
        print()

print("=" * 60)
print("\nUse one of the model names above (e.g., 'models/gemini-1.5-flash')")

