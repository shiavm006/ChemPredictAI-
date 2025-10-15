# ChemPredict AI Backend

FastAPI backend with Google Gemini-powered research chatbot for chemical reaction prediction and research assistance.

## Features

- **Chemical Reaction Prediction**: Predict reaction types, yields, and safety hazards
- **AI Research Assistant**: Google Gemini-powered chatbot with chemistry knowledge base
- **RAG (Retrieval-Augmented Generation)**: Context-aware responses using vector database
- **Conversation Memory**: Maintains chat history per session

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Google Gemini API Key (FREE!)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key
4. No credit card required! 🎉

### 3. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
cp env.example .env
```

Edit `.env` and add your Gemini API key:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 4. Run the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at: http://127.0.0.1:8000

## API Endpoints

### Health Check
```
GET /
```

### Reaction Prediction
```
POST /predict
Content-Type: application/json

{
  "reactant1": "CH3COOH",
  "reactant2": "C2H5OH"
}
```

### Single Compound Properties
```
POST /predict_single
Content-Type: application/json

{
  "compound": "H2O"
}
```

### Research Chat (Gemini-powered)
```
POST /chat
Content-Type: application/json

{
  "message": "What is esterification?",
  "session_id": "user-123"
}
```

### Clear Chat Session
```
POST /chat/clear?session_id=user-123
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Technology Stack

- **FastAPI**: Modern Python web framework
- **Google Gemini Pro**: FREE AI model for chemistry assistance
- **LangChain**: LLM orchestration and RAG
- **ChromaDB**: Vector database for knowledge storage
- **Pydantic**: Data validation

## Free Tier Limits

Google Gemini FREE tier includes:
- 60 requests per minute
- 1,500 requests per day
- Completely FREE for most applications!

## Troubleshooting

### Error: "Chatbot service is not available"

**Solution**: Make sure you've set the `GOOGLE_API_KEY` in your `.env` file.

```bash
# Check if .env file exists
ls -la .env

# Make sure it contains your API key
cat .env
```

### Error: "Module not found"

**Solution**: Install all dependencies:

```bash
pip install -r requirements.txt
```

### ChromaDB Issues

**Solution**: Delete the chroma_db directory and restart:

```bash
rm -rf chroma_db
uvicorn main:app --reload
```

## Chemistry Knowledge Base

The chatbot includes knowledge about:
- Esterification and hydrolysis reactions
- Oxidation and reduction mechanisms
- Substitution reactions
- Polymerization processes
- Chemical safety protocols
- Toxicity assessment
- Reaction yields and optimization

You can expand the knowledge base by editing `chat_service.py` and adding more `Document` objects.

## Development

### Adding More Chemistry Knowledge

Edit `chat_service.py`, find the `_load_knowledge_base` method, and add new documents:

```python
Document(
    page_content="Your chemistry knowledge here...",
    metadata={"source": "organic_chemistry", "topic": "your_topic", "category": "reactions"}
)
```

### Testing the Chat Endpoint

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is esterification?", "session_id": "test-1"}'
```

## Production Deployment

For production, consider:
1. Use environment variables for all sensitive data
2. Add rate limiting (already included in Gemini free tier)
3. Implement caching for common queries
4. Monitor API usage in Google AI Studio
5. Set up proper logging and error tracking

## License

© 2024 ChemPredict AI. All rights reserved.

