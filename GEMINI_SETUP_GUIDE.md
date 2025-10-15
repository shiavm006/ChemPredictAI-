# 🚀 Gemini Integration Setup Guide

## ✅ What's Been Implemented

Your ChemPredict AI now has a **Google Gemini-powered research chatbot** with:

- ✅ **Free AI Model**: Google Gemini Pro (60 requests/min FREE!)
- ✅ **Chemistry Knowledge Base**: Pre-loaded with reaction mechanisms and safety info
- ✅ **RAG System**: Retrieval-Augmented Generation for accurate responses
- ✅ **Conversation Memory**: Maintains chat history per session
- ✅ **Production Ready**: Error handling, rate limits, and proper architecture

## 📋 Quick Start (5 Minutes)

### Step 1: Get Your FREE Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key (starts with `AIza...`)
4. **No credit card required!** 🎉

### Step 2: Install Backend Dependencies

```bash
cd "ChemPredictAI/backend"

# Install all required packages
pip install -r requirements.txt
```

**Expected packages:**
- fastapi
- uvicorn
- langchain
- langchain-google-genai
- google-generativeai
- chromadb
- sentence-transformers
- python-dotenv

### Step 3: Configure API Key

Create a `.env` file in the `backend` directory:

```bash
# In backend directory
echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
```

**Replace `your_actual_api_key_here` with your real API key!**

### Step 4: Start the Backend

```bash
# Make sure you're in the backend directory
cd "ChemPredictAI/backend"

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
✅ ChemPredict AI Chatbot initialized successfully with Gemini Pro
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Start the Frontend

In a **new terminal**:

```bash
cd "ChemPredictAI/frontend"

# If not already installed
npm install

# Start the dev server
npm run dev
```

**Frontend will run on:** http://localhost:8080

### Step 6: Test the Chat!

1. Open http://localhost:8080 in your browser
2. Click **"Research Chat"** in the header
3. Ask a chemistry question like:
   - "What is esterification?"
   - "How do I calculate reaction yield?"
   - "What safety precautions are needed for oxidation reactions?"

## 🎯 What You Can Ask

The chatbot knows about:

- **Reactions**: Esterification, hydrolysis, oxidation, reduction, substitution, polymerization
- **Safety**: Lab protocols, toxicity assessment, hazard levels
- **Theory**: Acid-base chemistry, reaction yields, mechanisms
- **Practical**: Lab techniques, best practices

## 🧪 Example Questions

```
"What is the mechanism of esterification?"
→ Gets detailed explanation with acid catalyst requirement

"What safety equipment do I need for handling acids?"
→ Gets proper PPE recommendations and protocols

"How can I improve my reaction yield?"
→ Gets factors affecting yield and optimization tips

"Tell me about nucleophilic substitution"
→ Gets SN1 vs SN2 mechanisms explained
```

## 📊 API Endpoints Created

### Chat Endpoint
```bash
POST http://127.0.0.1:8000/chat
Content-Type: application/json

{
  "message": "What is esterification?",
  "session_id": "user-123"
}
```

### Clear Session
```bash
POST http://127.0.0.1:8000/chat/clear?session_id=user-123
```

### Test API Directly
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is esterification?", "session_id": "test"}'
```

## 💰 Cost & Limits (FREE Tier)

**Google Gemini Free Tier:**
- ✅ 60 requests per minute
- ✅ 1,500 requests per day
- ✅ Completely FREE
- ✅ No credit card required
- ✅ Perfect for development and small production apps

**When you need more:**
- Paid tier: $0.00025 per 1K characters (~10x cheaper than OpenAI!)

## 🔧 Troubleshooting

### Error: "Chatbot service is not available"

**Fix:** Check your .env file

```bash
cd backend
cat .env

# Should show:
# GOOGLE_API_KEY=AIza...
```

### Error: "Module not found: langchain"

**Fix:** Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Backend won't start

**Fix:** Check if virtual environment is activated

```bash
# Create venv if needed
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Then install and run
pip install -r requirements.txt
uvicorn main:app --reload
```

### Chat responses are slow

**Normal!** First response initializes the model (~3-5 seconds). Subsequent responses are faster (~1-2 seconds).

### ChromaDB errors

**Fix:** Delete and recreate the vector database

```bash
cd backend
rm -rf chroma_db
# Restart the server - it will recreate automatically
uvicorn main:app --reload
```

## 📝 Files Created/Modified

### Backend Files:
- ✅ `requirements.txt` - All Python dependencies
- ✅ `chat_service.py` - Gemini chatbot implementation
- ✅ `main.py` - Added `/chat` endpoint
- ✅ `env.example` - API key template
- ✅ `README.md` - Backend documentation

### Frontend Files:
- ✅ `ChemPredictChat.tsx` - Updated to call backend API

## 🎨 Features

### 1. Conversation Memory
Each user session maintains chat history:
```python
session_id = "user-123"  # Unique per user
```

### 2. Context-Aware Responses
Uses RAG to retrieve relevant chemistry knowledge before answering.

### 3. Source Attribution
Responses can include sources from the knowledge base.

### 4. Error Handling
Graceful fallbacks if API fails or limits are reached.

## 🚀 Next Steps

### 1. Expand Knowledge Base

Edit `backend/chat_service.py`, find `chemistry_knowledge` array, and add more documents:

```python
Document(
    page_content="Your chemistry knowledge here...",
    metadata={"source": "organic_chemistry", "topic": "alkenes", "category": "reactions"}
)
```

### 2. Add More Features

- File upload for chemical structures
- Export chat history
- Advanced search in past conversations
- Integration with PubChem API

### 3. Deploy to Production

See `backend/README.md` for deployment guides for:
- Railway.app
- Render.com
- Fly.io
- AWS Lambda

## 🎓 Learn More

- **Gemini API Docs**: https://ai.google.dev/docs
- **LangChain Docs**: https://python.langchain.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/

## 💡 Tips

1. **Keep API Key Secret**: Never commit `.env` to Git
2. **Monitor Usage**: Check usage at https://makersuite.google.com/
3. **Optimize Prompts**: Better prompts = better responses
4. **Cache Common Questions**: Save API calls for frequently asked questions
5. **Add More Knowledge**: The more context, the better the answers!

## ✅ Success Checklist

- [ ] Got Gemini API key from Google AI Studio
- [ ] Created `.env` file with API key
- [ ] Installed Python dependencies (`pip install -r requirements.txt`)
- [ ] Backend running on port 8000
- [ ] Frontend running on port 8080
- [ ] Can ask questions in Research Chat
- [ ] Getting relevant chemistry responses

## 🆘 Need Help?

If you encounter issues:

1. Check backend logs for errors
2. Verify API key is correct in `.env`
3. Ensure all dependencies are installed
4. Try the curl test command to isolate frontend vs backend issues
5. Check Google AI Studio for API quota/usage

---

**You're all set! 🎉**

Go to http://localhost:8080, click "Research Chat", and start asking chemistry questions powered by Google Gemini!

