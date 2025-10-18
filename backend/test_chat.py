"""
Test script for Gemini chatbot
Run this to verify your setup is working correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_key():
    """Test if API key is configured"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in .env file")
        print("TIP: Create a .env file and add: GOOGLE_API_KEY=your_key_here")
        return False
    print(f"SUCCESS: API Key found: {api_key[:10]}...")
    return True

def test_imports():
    """Test if all required packages are installed"""
    try:
        import langchain
        print("SUCCESS: langchain installed")
    except ImportError:
        print("ERROR: langchain not installed - run: pip install langchain")
        return False
    
    try:
        import langchain_google_genai
        print("SUCCESS: langchain-google-genai installed")
    except ImportError:
        print("ERROR: langchain-google-genai not installed - run: pip install langchain-google-genai")
        return False
    
    try:
        import chromadb
        print("SUCCESS: chromadb installed")
    except ImportError:
        print("ERROR: chromadb not installed - run: pip install chromadb")
        return False
    
    return True

def test_chatbot():
    """Test if chatbot can be initialized"""
    try:
        from chat_service import chatbot
        if chatbot is None:
            print("ERROR: Chatbot failed to initialize")
        return False
    print("SUCCESS: Chatbot initialized successfully")
    return True
except Exception as e:
    print(f"ERROR: Error initializing chatbot: {e}")
        return False

def test_chat_response():
    """Test if chatbot can respond to a query"""
    try:
        from chat_service import chatbot
        if chatbot is None:
            print("ERROR: Chatbot not available for testing")
            return False
        
        print("\nTesting chat response...")
        response = chatbot.chat("What is esterification?", "test-session")
        
        if response and "answer" in response:
            print("SUCCESS: Chat response received")
            print(f"Response preview: {response['answer'][:100]}...")
            return True
        else:
            print("ERROR: No valid response received")
            return False
    except Exception as e:
        print(f"ERROR: Error testing chat: {e}")
        return False

def main():
    print("Testing setup...")
    
    tests = [
        ("API Key", test_api_key),
        ("Dependencies", test_imports),
        ("Chatbot", test_chatbot),
        ("Chat", test_chat_response)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"Testing {name}...")
        results.append(test_func())
    
    passed = sum(results)
    print(f"\nResult: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("All good! Run 'uvicorn main:app --reload' to start")
    else:
        print("Some tests failed, check errors above")

if __name__ == "__main__":
    main()

