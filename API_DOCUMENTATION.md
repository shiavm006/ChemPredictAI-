# ChemPredictAI API Documentation

## Base URL
- **Production**: `https://chempredict-ai-backend.onrender.com`
- **Local Development**: `http://localhost:8000`

## API Endpoints

### 1. Health Check
**GET** `/`

Check if the API is running.

**Response:**
```json
{
  "message": "ChemPredict AI API is running"
}
```

### 2. Predict Reaction (ML Models)
**POST** `/predict_all`

Predict chemical reaction using trained ML models on 31k+ chemical reactions.

**Request Body:**
```json
{
  "reactant1": "ethanol",
  "reactant2": "acetic acid"
}
```

**Response:**
```json
{
  "reaction_type": "Esterification",
  "product": "Ethyl acetate",
  "safety_hazard_level": "Medium",
  "reaction_description": "This is an esterification reaction between ethanol and acetic acid, producing ethyl acetate and water. The reaction is catalyzed by acid and typically occurs at elevated temperatures. Ethyl acetate is a common solvent with moderate toxicity and flammability.",
  "predicted_yield": "85%",
  "reactant1_smiles": "CCO",
  "reactant2_smiles": "CC(=O)O",
  "product_smiles": "CCOC(=O)C",
  "prediction_method": "ml_model"
}
```


### 4. Research Chat
**POST** `/chat`

Interactive chat with chemistry research assistant powered by LangChain and Gemini API.

**Request Body:**
```json
{
  "message": "What is the mechanism of esterification?",
  "session_id": "user123"
}
```

**Response:**
```json
{
  "response": "Esterification is a chemical reaction between a carboxylic acid and an alcohol, typically catalyzed by an acid. The mechanism involves...",
  "sources": [
    {
      "title": "Organic Chemistry Textbook",
      "url": "https://example.com/esterification",
      "relevance": 0.95
    }
  ],
  "session_id": "user123",
  "timestamp": "2024-01-15T10:30:00Z",
  "model": "gemini-2.5-flash"
}
```

### 5. Clear Chat Session
**POST** `/chat/clear`

Clear the chat session history.

**Request Body:**
```json
{
  "session_id": "user123"
}
```

**Response:**
```json
{
  "message": "Session user123 cleared"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 503 Service Unavailable
```json
{
  "detail": "ML model not available. Install dependencies or add RXN4CHEMISTRY_API_KEY to .env"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error in ML prediction: [error details]"
}
```

## Response Fields

### Reaction Prediction Fields
- **reaction_type**: Type of chemical reaction (e.g., "Substitution", "Elimination")
- **product**: Predicted main product name
- **safety_hazard_level**: Safety assessment ("Low", "Medium", "High")
- **reaction_description**: Detailed explanation of the reaction
- **predicted_yield**: Expected yield percentage
- **reactant1_smiles**: SMILES notation for first reactant
- **reactant2_smiles**: SMILES notation for second reactant
- **product_smiles**: SMILES notation for predicted product
- **prediction_method**: Method used ("ml_model" or "gemini-2.5-flash")

### Chat Response Fields
- **response**: AI assistant's response
- **sources**: Array of source references
- **session_id**: Unique session identifier
- **timestamp**: Response timestamp (ISO format)
- **model**: AI model used for response

## Example Usage

### Python Example
```python
import requests
import json

# API base URL
BASE_URL = "https://chempredict-ai-backend.onrender.com"

# Predict reaction
def predict_reaction(reactant1, reactant2):
    response = requests.post(f"{BASE_URL}/predict_all", json={
        "reactant1": reactant1,
        "reactant2": reactant2
    })
    return response.json()

# Example usage
result = predict_reaction("methanol", "formic acid")
print(f"Product: {result['product']}")
print(f"Reaction Type: {result['reaction_type']}")
print(f"Hazard Level: {result['safety_hazard_level']}")
```

### JavaScript Example
```javascript
// Predict reaction
async function predictReaction(reactant1, reactant2) {
    const response = await fetch('https://chempredict-ai-backend.onrender.com/predict_all', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            reactant1: reactant1,
            reactant2: reactant2
        })
    });
    return await response.json();
}

// Example usage
predictReaction('ethanol', 'acetic acid')
    .then(result => {
        console.log('Product:', result.product);
        console.log('Reaction Type:', result.reaction_type);
        console.log('Hazard Level:', result.safety_hazard_level);
    });
```

### cURL Examples
```bash
# Health check
curl -X GET "https://chempredict-ai-backend.onrender.com/"

# Predict reaction
curl -X POST "https://chempredict-ai-backend.onrender.com/predict_all" \
  -H "Content-Type: application/json" \
  -d '{"reactant1": "benzene", "reactant2": "chlorine"}'

# Chat with AI
curl -X POST "https://chempredict-ai-backend.onrender.com/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain SN2 mechanism", "session_id": "user123"}'
```

## 🔒 Authentication

Currently, the API does not require authentication. Rate limiting is applied:
- **Rate Limit**: 60 requests per minute
- **Token Limit**: 2000 tokens per request
- **Session Timeout**: 30 minutes

## Rate Limits

| Endpoint | Rate Limit | Token Limit |
|----------|------------|-------------|
| `/predict_all` | 60/min | 2000 tokens |
| `/chat` | 60/min | 2000 tokens |
| `/chat/clear` | 60/min | N/A |

## Current Limitations

### ML Model Status
- **Local Development**: Fully functional
- **Production Deployment**: In progress
- **Current Mode**: LLM-only predictions

### Dataset Access
The trained dataset (31k+ chemical reactions) used for model training is available at: [Google Drive Link](https://drive.google.com/drive/folders/1frpLZMOvq0Vh7FrUdwUDVY-VYli8xpuD?usp=sharing)

### Known Issues
1. **ML Models**: Not yet deployed to production
2. **Build Dependencies**: Complex chemistry packages causing build issues
3. **Model Size**: Large model files requiring optimization

### Workarounds
- Local development includes full ML functionality
- Production will have ML models available soon
- Research chat works with LangChain and Gemini API

## Status Updates

### Deployment Status
- **Backend API**: Deployed and functional
- **Frontend**: Deployed and functional  
- **ML Models**: Building phase
- **Database**: ChromaDB vector database active

### Expected Timeline
- **ML Model Deployment**: 1-2 weeks
- **Full Feature Set**: 2-3 weeks
- **Performance Optimization**: 3-4 weeks

## Support

For API issues or questions:
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check this file for updates
- **Status Page**: Monitor deployment status
- **Email**: api-support@chempredict.ai

---

**Note**: The ML models are currently in the building phase for production deployment. They work perfectly in local development and will be available in production soon. The LLM-based prediction system is fully functional and provides excellent results for chemical reaction prediction.
