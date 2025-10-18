# ChemPredictAI

A chemical reaction prediction system that combines ML models with LLMs to predict reaction outcomes, products, and safety hazards.

## What this does

Started this project to solve a real problem in chemistry research - predicting reaction outcomes before running expensive lab experiments. Trained ML models on 31k+ chemical reactions and integrated with Google's Gemini API.

The system takes two reactants (like "ethanol" and "acetic acid") and predicts:
- What product will form
- What type of reaction it is  
- How dangerous it is
- Detailed explanation of the mechanism

## Tech stack

**Backend:**
- FastAPI for the API
- Python + scikit-learn for ML models
- Google Gemini API for reasoning
- ChromaDB for chemical knowledge storage
- LangChain for chat

**Frontend:**
- React + TypeScript
- Tailwind CSS
- Real-time chat interface

**ML stuff:**
- 3 separate models trained on chemical reaction data
- SMILES molecular representation
- Feature engineering for chemical properties
- Ensemble methods work best

## Data & Models

Collected 31k+ chemical reactions from various sources. Spent way too much time cleaning and preprocessing the data. The biggest pain was standardizing SMILES notation and handling different naming conventions.

**Trained dataset available here:** [Google Drive Link](https://drive.google.com/drive/folders/1frpLZMOvq0Vh7FrUdwUDVY-VYli8xpuD?usp=sharing)

**Models trained:**
1. **Reaction Type Classifier** - substitution, elimination, addition, etc. (85% accuracy)
2. **Hazard Level Predictor** - safety risk Low/Medium/High (80% accuracy)  
3. **Product Predictor** - what the main product will be (75% accuracy)

Used molecular fingerprints and chemical descriptors as features. Tried different algorithms, ensemble methods work best for this data.

## How it works

1. User enters two chemicals (e.g., "ethanol" + "acetic acid")
2. Convert names to SMILES, extract molecular features
3. Run through trained models to get reaction type, hazard level, and product
4. Gemini adds detailed explanations and safety info
5. Return complete prediction with mechanism explanation

The tricky part was getting ML models and LLM to work together. ML models give the "what", Gemini explains the "why" and "how".

## Current status

**Working:**
- Backend API deployed and running
- Frontend is live
- Chat system works
- LLM predictions are operational

**Still working on:**
ML models work great locally but having deployment issues. Chemistry libraries (like RDKit) are huge and don't play nice with cloud deployment. Working on optimizing the build process.

**For now:**
You can test everything locally - ML models work perfectly on your machine. Deployed version uses Gemini for predictions, which actually gives good results too.

## Try It Locally

**Setup:**
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add your API keys to .env file
echo "GOOGLE_API_KEY=your_key_here" > .env

# Run backend
uvicorn main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

**Test the ML models:**
```python
# This will work locally with full ML functionality
from ML_Model.predict.predict_reaction import predict_reaction
result = predict_reaction("ethanol", "acetic acid", input_type="name")
print(result)
```

## What I Learned

**Technical Challenges:**
- SMILES notation standardization was a nightmare
- Getting RDKit to work with different Python versions  
- Balancing ML accuracy with response time
- Integrating multiple APIs (Gemini, RXN4Chemistry)

**ML Insights:**
- Chemical data is messy - lots of cleaning required
- Ensemble methods work better than single models
- Feature engineering is crucial for chemical properties
- LLMs can actually help explain ML predictions

**Deployment Lessons:**
- Chemistry libraries are huge and complex
- Cloud deployment has different constraints than local
- Sometimes simpler solutions (LLM-only) work just as well

## API Usage

**Main endpoints:**
- `/predict_all` - Full ML + LLM prediction
- `/predict_product_llm` - LLM-only prediction  
- `/chat` - Ask chemistry questions

**Example:**
```python
import requests

response = requests.post("http://localhost:8000/predict_all", json={
    "reactant1": "benzene", 
    "reactant2": "nitric acid"
})

result = response.json()
print(f"Product: {result['product']}")
print(f"Reaction Type: {result['reaction_type']}")
```

## Technical Details

**Data Processing:**
I spent a lot of time cleaning the chemical data - standardizing SMILES notation, handling different naming conventions, and dealing with incomplete reactions. The data came from multiple sources so consistency was a big challenge.

**Model Architecture:**
- Random Forest for reaction type classification
- Gradient Boosting for hazard level prediction  
- Neural network for product prediction
- Cross-validation to avoid overfitting

**Performance:**
- Reaction type: 85% accuracy
- Hazard level: 80% accuracy
- Product prediction: 75% accuracy

## Why I Built This

I wanted to solve a real problem in chemistry research - predicting reaction outcomes before running expensive lab experiments. This could help:

- **Researchers** predict if a reaction will work
- **Students** understand reaction mechanisms  
- **Industry** assess safety risks before scaling up
- **Anyone** learn about chemical reactions

The chat feature lets you ask questions like "What happens if I mix X and Y?" and get detailed explanations.

## Next Steps

**What I'm working on:**
- Fixing the deployment issues with the ML models
- Adding more reaction types to the dataset
- Improving the chat interface
- Maybe adding 3D molecule visualization

**Try it out:**
The system works great locally with full ML functionality. The deployed version uses Gemini for predictions, which actually gives really good results too.

**Contact:**
Feel free to reach out if you want to collaborate or have questions about the implementation!
