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
        print("❌ GOOGLE_API_KEY not found in .env file")
        print("💡 Create a .env file and add: GOOGLE_API_KEY=your_key_here")
        return False
    print(f"✅ API Key found: {api_key[:10]}...")
    return True

def test_imports():
    """Test if all required packages are installed"""
    try:
        import langchain
        print("✅ langchain installed")
    except ImportError:
        print("❌ langchain not installed - run: pip install langchain")
        return False
    
    try:
        import langchain_google_genai
        print("✅ langchain-google-genai installed")
    except ImportError:
        print("❌ langchain-google-genai not installed - run: pip install langchain-google-genai")
        return False
    
    try:
        import chromadb
        print("✅ chromadb installed")
    except ImportError:
        print("❌ chromadb not installed - run: pip install chromadb")
        return False
    
    return True

def test_chatbot():
    """Test if chatbot can be initialized"""
    try:
        from chat_service import chatbot
        if chatbot is None:
            print("❌ Chatbot failed to initialize")
            return False
        print("✅ Chatbot initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        return False

def test_chat_response():
    """Test if chatbot can respond to a query"""
    try:
        from chat_service import chatbot
        if chatbot is None:
            print("❌ Chatbot not available for testing")
            return False
        
        print("\n🧪 Testing chat response...")
        response = chatbot.chat("What is esterification?", "test-session")
        
        if response and "answer" in response:
            print("✅ Chat response received")
            print(f"📝 Response preview: {response['answer'][:100]}...")
            return True
        else:
            print("❌ No valid response received")
            return False
    except Exception as e:
        print(f"❌ Error testing chat: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 ChemPredict AI - Gemini Setup Test")
    print("=" * 60)
    print()
    
    tests = [
        ("API Key Configuration", test_api_key),
        ("Package Installation", test_imports),
        ("Chatbot Initialization", test_chatbot),
        ("Chat Response", test_chat_response)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n📋 Testing: {name}")
        print("-" * 60)
        results.append(test_func())
        print()
    
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready!")
        print("📝 Next step: Run 'uvicorn main:app --reload' to start the server")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above and try again.")
        print("💡 Check GEMINI_SETUP_GUIDE.md for troubleshooting help")

if __name__ == "__main__":
    main()

