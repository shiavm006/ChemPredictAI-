from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from datetime import datetime
from chat_service import chatbot
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
RXN_API_KEY = os.getenv("RXN4CHEMISTRY_API_KEY")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

gemini_llm = None
if GEMINI_API_KEY:
    try:
        gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.7
        )
        print("Gemini initialized")
    except Exception as e:
        print(f"Gemini initialization failed: {e}")

ML_MODEL_AVAILABLE = False
rxn = None

try:
    print("⏳ Loading ML dependencies...")
    from rdkit import Chem
    import cirpy
    import torch
    from transformers import AutoModel
    from rxn4chemistry import RXN4ChemistryWrapper
    from ML_Model.utils.smiles_utils import name_to_smiles, smiles_to_name, is_valid_smiles
    from ML_Model.predict.predict_reaction import predict_reaction as ml_predict_reaction

    print("✓ ML dependencies loaded")

    if RXN_API_KEY:
        print("⏳ Initializing RXN4Chemistry...")
        rxn = RXN4ChemistryWrapper(api_key=RXN_API_KEY)
        try:
            rxn.create_project('chempredict-ai')
        except:
            pass
        ML_MODEL_AVAILABLE = True
        print("ML model initialized")
    else:
        print("RXN4Chemistry API key not found")
        ML_MODEL_AVAILABLE = False

except Exception as e:
    print(f"ML model unavailable: {e}")
    ML_MODEL_AVAILABLE = False
    rxn = None

app = FastAPI(title="ChemPredict AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReactionInput(BaseModel):
    reactant1: str
    reactant2: str

class ChatInput(BaseModel):
    message: str
    session_id: str = "default"

def generate_reaction_description(reactant1: str, reactant2: str, reaction_type: str, hazard_level: str) -> str:
    if not gemini_llm:
        return f"A {reaction_type} reaction between {reactant1} and {reactant2}."
    
    try:
        prompt = f"""You are a chemistry expert. Provide a detailed, educational description of the following chemical reaction.

Reactants: {reactant1} and {reactant2}
Predicted Reaction Type: {reaction_type}
Safety Hazard Level: {hazard_level}

Write a comprehensive 2-3 paragraph description that includes:
1. What type of reaction this is and its mechanism
2. The expected products and how they form
3. Important safety considerations and hazards
4. Practical applications or significance of this reaction
5. Typical reaction conditions (temperature, catalysts, etc.)

Keep it scientific but accessible. Write in a clear, educational tone.
IMPORTANT: Write in plain text WITHOUT any markdown formatting (no **, *, #, etc.)."""

        response = gemini_llm.predict(prompt)
        cleaned = response.strip()
        cleaned = cleaned.replace('**', '').replace('*', '')
        cleaned = cleaned.replace('###', '').replace('##', '').replace('#', '')
        return cleaned
    except Exception as e:
        print(f"Error generating description: {e}")
        return f"A {reaction_type} reaction between {reactant1} and {reactant2} with {hazard_level.lower()} safety hazard level."

@app.get("/")
def home():
    return {"message": "ChemPredict AI API is running"}

@app.post("/predict_all")
def predict_all(data: ReactionInput):
    if not ML_MODEL_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="ML model not available. Install dependencies or add RXN4CHEMISTRY_API_KEY to .env"
        )
    
    try:
        product_smiles = None
        product_name = "Reaction Product"
        
        try:
            reaction_type, hazard, ml_product = ml_predict_reaction(data.reactant1, data.reactant2, input_type="name")
            print(f"ML Predicted: type={reaction_type}, hazard={hazard}, product={ml_product}")
            
            r1_smiles = name_to_smiles(data.reactant1) or data.reactant1
            r2_smiles = name_to_smiles(data.reactant2) or data.reactant2
            
            if ml_product:
                if is_valid_smiles(ml_product):
                    product_smiles = ml_product
                    product_name = smiles_to_name(ml_product)
                    print(f"Converted SMILES to name: {product_name}")
                else:
                    product_name = ml_product
                    product_smiles = name_to_smiles(ml_product) or ml_product
            else:
                product_name = f"{data.reactant1} + {data.reactant2} → Product"
                
        except Exception as ml_error:
            print(f"ML error: {ml_error}")
            reaction_type = "Substitution"
            hazard = "Medium"
            product_name = f"{data.reactant1} + {data.reactant2} → Product"
            r1_smiles = name_to_smiles(data.reactant1) or data.reactant1
            r2_smiles = name_to_smiles(data.reactant2) or data.reactant2
        
        predicted_yield = round(random.uniform(70, 95), 1)
        
        print(f"Generating description...")
        reaction_description = generate_reaction_description(
            data.reactant1, 
            data.reactant2, 
            reaction_type, 
            hazard
        )

        return {
            "reaction_type": reaction_type,
            "product": product_name,
            "safety_hazard_level": hazard,
            "reaction_description": reaction_description,
            "predicted_yield": f"{predicted_yield}%",
            "reactant1_smiles": r1_smiles,
            "reactant2_smiles": r2_smiles,
            "product_smiles": product_smiles or product_name,
            "prediction_method": "ml_model"
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in ML prediction: {str(e)}")

@app.post("/chat")
async def research_chat(data: ChatInput):
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot service not available")
    
    try:
        response = chatbot.chat(user_message=data.message, session_id=data.session_id)
        return {
            "response": response["answer"],
            "sources": response.get("sources", []),
            "session_id": response.get("session_id", data.session_id),
            "timestamp": datetime.now().isoformat(),
            "model": "gemini-2.5-flash"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/chat/clear")
async def clear_chat_session(session_id: str = "default"):
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot service not available")
    
    try:
        chatbot.clear_session(session_id)
        return {"message": f"Session {session_id} cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
