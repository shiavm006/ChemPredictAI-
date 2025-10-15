"""
Simple test to check if Gemini API is working
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Gemini API connection...")

# Test 1: Check API key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print(f"✓ API key found: {api_key[:10]}...{api_key[-4:]}")
else:
    print("✗ No API key found!")
    exit(1)

# Test 2: Try direct Gemini API call
try:
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("\nSending test message to Gemini...")
    response = model.generate_content("Say hello in one short sentence")
    
    print(f"✓ Response received: {response.text}")
    print("\n✓ Gemini API is working!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Test 3: Try LangChain
try:
    print("\nTesting LangChain integration...")
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.7,
        convert_system_message_to_human=True
    )
    
    result = llm.predict("Say hello in one short sentence")
    print(f"✓ LangChain response: {result}")
    print("\n✓ LangChain is working!")
    
except Exception as e:
    print(f"✗ LangChain error: {e}")
    exit(1)

print("\n" + "="*50)
print("ALL TESTS PASSED! Backend should work.")
print("="*50)

