from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

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

@app.get("/")
def home():
    return {"message": "ChemPredict AI API is running"}

@app.post("/predict")
def predict(data: ReactionInput):
    outcomes = ["Esterification", "Hydrogenation", "Oxidation", "Substitution", "Polymerization"]
    predicted = random.choice(outcomes)
    yield_percent = round(random.uniform(60, 98), 2)
    return {
        "reaction_type": predicted,
        "predicted_yield": f"{yield_percent}%"
    }
    