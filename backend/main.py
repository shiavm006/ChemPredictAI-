from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from datetime import datetime
from chat_service import chatbot

app = FastAPI(title="ChemPredict AI")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReactionInput(BaseModel):
    reactant1: str
    reactant2: str

class CompoundInput(BaseModel):
    compound: str

class ChatInput(BaseModel):
    message: str
    session_id: str = "default"

@app.get("/")
def home():
    return {"message": "ChemPredict AI API is running"}

@app.post("/predict")
def predict(data: ReactionInput):
    reactant1 = data.reactant1.lower()
    reactant2 = data.reactant2.lower()
    
    # Define realistic reaction scenarios
    reactions = {
        "esterification": {
            "reaction_type": "Esterification",
            "product": "Ethyl Acetate",
            "safety_hazard_level": "Low",
            "reaction_description": "A condensation reaction between an acid and alcohol in the presence of a catalyst, typically producing an ester and water. This reaction is commonly used in organic synthesis and is generally safe when proper precautions are taken.",
            "predicted_yield": round(random.uniform(75, 95), 1)
        },
        "hydrolysis": {
            "reaction_type": "Hydrolysis",
            "product": "Salt and Water",
            "safety_hazard_level": "Low",
            "reaction_description": "A decomposition reaction where water breaks down a compound into simpler substances. This is a fundamental reaction in biochemistry and industrial processes.",
            "predicted_yield": round(random.uniform(80, 98), 1)
        },
        "oxidation": {
            "reaction_type": "Oxidation",
            "product": "Oxidized Compound",
            "safety_hazard_level": "Medium",
            "reaction_description": "A chemical reaction where electrons are lost, often involving oxygen or other oxidizing agents. Can be exothermic and may require careful temperature control.",
            "predicted_yield": round(random.uniform(60, 85), 1)
        },
        "reduction": {
            "reaction_type": "Reduction",
            "product": "Reduced Compound",
            "safety_hazard_level": "Medium",
            "reaction_description": "A chemical reaction where electrons are gained, typically using reducing agents. Often requires inert atmosphere and careful handling of reactive materials.",
            "predicted_yield": round(random.uniform(65, 90), 1)
        },
        "substitution": {
            "reaction_type": "Substitution",
            "product": "Substituted Compound",
            "safety_hazard_level": "Low",
            "reaction_description": "A reaction where one functional group is replaced by another. Common in organic chemistry and generally safe with proper solvent handling.",
            "predicted_yield": round(random.uniform(70, 92), 1)
        },
        "polymerization": {
            "reaction_type": "Polymerization",
            "product": "Polymer",
            "safety_hazard_level": "High",
            "reaction_description": "A reaction where monomers combine to form long polymer chains. Can be highly exothermic and requires strict temperature control and safety measures.",
            "predicted_yield": round(random.uniform(85, 98), 1)
        }
    }
    
    # Simple logic to determine reaction type based on reactants
    if any(acid in reactant1 for acid in ["acid", "hcl", "h2so4", "ch3cooh", "acetic"]) and any(alcohol in reactant2 for alcohol in ["oh", "ethanol", "methanol"]):
        selected_reaction = reactions["esterification"]
    elif any(water in reactant1 or water in reactant2 for water in ["h2o", "water"]):
        selected_reaction = reactions["hydrolysis"]
    elif any(oxidizer in reactant1 or oxidizer in reactant2 for oxidizer in ["o2", "oxygen", "h2o2", "peroxide"]):
        selected_reaction = reactions["oxidation"]
    elif any(reducer in reactant1 or reducer in reactant2 for reducer in ["h2", "hydrogen", "na", "sodium"]):
        selected_reaction = reactions["reduction"]
    elif any(monomer in reactant1 or monomer in reactant2 for monomer in ["ethene", "ethylene", "propene"]):
        selected_reaction = reactions["polymerization"]
    else:
        # Random selection for unknown combinations
        selected_reaction = random.choice(list(reactions.values()))
    
    return {
        "reaction_type": selected_reaction["reaction_type"],
        "product": selected_reaction["product"],
        "safety_hazard_level": selected_reaction["safety_hazard_level"],
        "reaction_description": selected_reaction["reaction_description"],
        "predicted_yield": f"{selected_reaction['predicted_yield']}%"
    }

@app.post("/predict_single")
def predict_single_compound(data: CompoundInput):
    compound = data.compound.lower()
    
    # Simulate AI prediction with realistic ranges based on compound type
    if "h2o" in compound or "water" in compound:
        return {
            "compound_name": "Water",
            "molecular_formula": "H₂O",
            "boiling_point": "100°C",
            "melting_point": "0°C", 
            "toxicity_level": "Low",
            "reactivity_index": "0.8"
        }
    elif "nacl" in compound or "sodium chloride" in compound:
        return {
            "compound_name": "Sodium Chloride",
            "molecular_formula": "NaCl",
            "boiling_point": "1413°C",
            "melting_point": "801°C",
            "toxicity_level": "Low", 
            "reactivity_index": "0.3"
        }
    elif "co2" in compound or "carbon dioxide" in compound:
        return {
            "compound_name": "Carbon Dioxide",
            "molecular_formula": "CO₂",
            "boiling_point": "-78.5°C",
            "melting_point": "-56.6°C",
            "toxicity_level": "Low",
            "reactivity_index": "0.2"
        }
    elif "ch4" in compound or "methane" in compound:
        return {
            "compound_name": "Methane",
            "molecular_formula": "CH₄", 
            "boiling_point": "-161.5°C",
            "melting_point": "-182.5°C",
            "toxicity_level": "Low",
            "reactivity_index": "0.1"
        }
    elif "h2so4" in compound or "sulfuric acid" in compound:
        return {
            "compound_name": "Sulfuric Acid",
            "molecular_formula": "H₂SO₄",
            "boiling_point": "337°C", 
            "melting_point": "10°C",
            "toxicity_level": "High",
            "reactivity_index": "4.2"
        }
    elif "naoh" in compound or "sodium hydroxide" in compound:
        return {
            "compound_name": "Sodium Hydroxide",
            "molecular_formula": "NaOH",
            "boiling_point": "1390°C",
            "melting_point": "318°C", 
            "toxicity_level": "Medium",
            "reactivity_index": "3.8"
        }
    else:
        # Generate random realistic values for unknown compounds
        boiling = round(random.uniform(-200, 2000), 1)
        melting = round(random.uniform(-250, 1500), 1)
        toxicity_levels = ["Low", "Medium", "High"]
        toxicity = random.choice(toxicity_levels)
        reactivity = round(random.uniform(0.1, 5.0), 1)
        
        return {
            "compound_name": data.compound.title(),
            "molecular_formula": data.compound.upper(),
            "boiling_point": f"{boiling}°C",
            "melting_point": f"{melting}°C",
            "toxicity_level": toxicity,
            "reactivity_index": str(reactivity)
        }

@app.post("/chat")
async def research_chat(data: ChatInput):
    """
    Research chat endpoint powered by Google Gemini
    Provides chemistry research assistance using RAG and conversation memory
    """
    if chatbot is None:
        raise HTTPException(
            status_code=503,
            detail="Chatbot service is not available. Please check GOOGLE_API_KEY environment variable."
        )
    
    try:
        # Get response from Gemini-powered chatbot
        response = chatbot.chat(
            user_message=data.message,
            session_id=data.session_id
        )
        
        return {
            "response": response["answer"],
            "sources": response.get("sources", []),
            "session_id": response.get("session_id", data.session_id),
            "timestamp": datetime.now().isoformat(),
            "model": "gemini-2.5-flash"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )

@app.post("/chat/clear")
async def clear_chat_session(session_id: str = "default"):
    """Clear conversation history for a session"""
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot service not available")
    
    try:
        chatbot.clear_session(session_id)
        return {"message": f"Session {session_id} cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    