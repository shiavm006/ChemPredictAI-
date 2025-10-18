# Local Testing Guide for ChemPredictAI

## Testing the ML Models Locally

Since the ML models are currently in the building phase for deployment, you can test them locally to see the full functionality.

**Dataset Access:** The trained dataset (31k+ chemical reactions) is available at: [Google Drive Link](https://drive.google.com/drive/folders/1frpLZMOvq0Vh7FrUdwUDVY-VYli8xpuD?usp=sharing)

## Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd ChemPredictAI
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Create `.env` file in backend directory:
```env
GOOGLE_API_KEY=your_gemini_api_key
RXN4CHEMISTRY_API_KEY=your_rxn_api_key
```

### 4. Run Backend
```bash
uvicorn main:app --reload
```

### 5. Frontend Setup (Optional)
```bash
cd frontend
npm install
npm run dev
```

## Testing ML Models

### Test 1: Basic ML Prediction
```python
# test_ml_prediction.py
from ML_Model.predict.predict_reaction import predict_reaction

# Test reaction prediction
result = predict_reaction("ethanol", "acetic acid", input_type="name")
print("ML Prediction Result:")
print(f"Reaction Type: {result[0]}")
print(f"Hazard Level: {result[1]}")
print(f"Product: {result[2]}")
```

### Test 2: API Endpoints
```python
# test_api.py
import requests
import json

BASE_URL = "http://localhost:8000"

# Test health check
response = requests.get(f"{BASE_URL}/")
print("Health Check:", response.json())

# Test ML prediction
response = requests.post(f"{BASE_URL}/predict_all", json={
    "reactant1": "benzene",
    "reactant2": "nitric acid"
})
print("ML Prediction:", response.json())

# Test LLM prediction
response = requests.post(f"{BASE_URL}/predict_product_llm", json={
    "reactant1": "methanol",
    "reactant2": "formic acid"
})
print("LLM Prediction:", response.json())
```

### Test 3: Chat Interface
```python
# test_chat.py
import requests

BASE_URL = "http://localhost:8000"

# Test chat functionality
response = requests.post(f"{BASE_URL}/chat", json={
    "message": "What is the mechanism of esterification?",
    "session_id": "test123"
})
print("Chat Response:", response.json())
```

## ML Model Testing

### Test Individual Models
```python
# test_individual_models.py
import joblib
import pandas as pd

# Load trained models
reaction_type_model = joblib.load('ML_Model/models/reaction_type_model.pkl')
hazard_level_model = joblib.load('ML_Model/models/hazard_level_model.pkl')

# Test reaction type prediction
test_data = pd.DataFrame({
    'reactant1_smiles': ['CCO'],  # ethanol
    'reactant2_smiles': ['CC(=O)O']  # acetic acid
})

reaction_type = reaction_type_model.predict(test_data)
print(f"Predicted Reaction Type: {reaction_type[0]}")

# Test hazard level prediction
hazard_level = hazard_level_model.predict(test_data)
print(f"Predicted Hazard Level: {hazard_level[0]}")
```

### Test SMILES Conversion
```python
# test_smiles_conversion.py
from ML_Model.utils.smiles_utils import name_to_smiles, smiles_to_name, is_valid_smiles

# Test name to SMILES
ethanol_smiles = name_to_smiles("ethanol")
print(f"Ethanol SMILES: {ethanol_smiles}")

# Test SMILES to name
ethanol_name = smiles_to_name("CCO")
print(f"SMILES to Name: {ethanol_name}")

# Test SMILES validation
is_valid = is_valid_smiles("CCO")
print(f"Is valid SMILES: {is_valid}")
```

## Performance Testing

### Test Response Times
```python
# test_performance.py
import time
import requests

BASE_URL = "http://localhost:8000"

def test_response_time(endpoint, data):
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/{endpoint}", json=data)
    end_time = time.time()
    
    return {
        "endpoint": endpoint,
        "response_time": end_time - start_time,
        "status_code": response.status_code,
        "success": response.status_code == 200
    }

# Test different endpoints
tests = [
    ("predict_all", {"reactant1": "benzene", "reactant2": "chlorine"}),
    ("predict_product_llm", {"reactant1": "methanol", "reactant2": "formic acid"}),
    ("chat", {"message": "Explain SN2 mechanism", "session_id": "test123"})
]

for endpoint, data in tests:
    result = test_response_time(endpoint, data)
    print(f"{endpoint}: {result['response_time']:.2f}s - {'PASS' if result['success'] else 'FAIL'}")
```

### Test Accuracy
```python
# test_accuracy.py
import requests

BASE_URL = "http://localhost:8000"

# Test cases with known outcomes
test_cases = [
    {
        "reactant1": "ethanol",
        "reactant2": "acetic acid",
        "expected_product": "ethyl acetate",
        "expected_type": "esterification"
    },
    {
        "reactant1": "benzene",
        "reactant2": "nitric acid",
        "expected_product": "nitrobenzene",
        "expected_type": "nitration"
    }
]

for test_case in test_cases:
    response = requests.post(f"{BASE_URL}/predict_all", json={
        "reactant1": test_case["reactant1"],
        "reactant2": test_case["reactant2"]
    })
    
    result = response.json()
    print(f"Test: {test_case['reactant1']} + {test_case['reactant2']}")
    print(f"Predicted Product: {result['product']}")
    print(f"Predicted Type: {result['reaction_type']}")
    print(f"Expected Product: {test_case['expected_product']}")
    print(f"Expected Type: {test_case['expected_type']}")
    print("---")
```

## Chemical Reaction Tests

### Test Common Reactions
```python
# test_common_reactions.py
import requests

BASE_URL = "http://localhost:8000"

common_reactions = [
    ("methanol", "formic acid", "Methyl formate"),
    ("ethanol", "acetic acid", "Ethyl acetate"),
    ("benzene", "chlorine", "Chlorobenzene"),
    ("ethene", "hydrogen", "Ethane"),
    ("propene", "water", "Propanol")
]

for reactant1, reactant2, expected in common_reactions:
    response = requests.post(f"{BASE_URL}/predict_all", json={
        "reactant1": reactant1,
        "reactant2": reactant2
    })
    
    result = response.json()
    print(f"{reactant1} + {reactant2} → {result['product']}")
    print(f"Expected: {expected}")
    print(f"Reaction Type: {result['reaction_type']}")
    print(f"Hazard Level: {result['safety_hazard_level']}")
    print("---")
```

### Test Hazard Level Predictions
```python
# test_hazard_levels.py
import requests

BASE_URL = "http://localhost:8000"

hazard_test_cases = [
    ("water", "salt", "Low"),  # Should be low hazard
    ("benzene", "nitric acid", "High"),  # Should be high hazard
    ("ethanol", "acetic acid", "Medium")  # Should be medium hazard
]

for reactant1, reactant2, expected_hazard in hazard_test_cases:
    response = requests.post(f"{BASE_URL}/predict_all", json={
        "reactant1": reactant1,
        "reactant2": reactant2
    })
    
    result = response.json()
    actual_hazard = result['safety_hazard_level']
    match = "PASS" if actual_hazard.lower() == expected_hazard.lower() else "FAIL"
    
    print(f"{reactant1} + {reactant2}")
    print(f"Expected Hazard: {expected_hazard}")
    print(f"Predicted Hazard: {actual_hazard} {match}")
    print("---")
```

## Debugging

### Check ML Model Status
```python
# check_ml_status.py
import os
import joblib

def check_ml_models():
    models_dir = "ML_Model/models"
    
    required_files = [
        "reaction_type_model.pkl",
        "hazard_level_model.pkl",
        "reaction_type_encoder.pkl",
        "hazard_level_encoder.pkl"
    ]
    
    print("Checking ML Model Files:")
    for file in required_files:
        file_path = os.path.join(models_dir, file)
        exists = os.path.exists(file_path)
        print(f"{file}: {'EXISTS' if exists else 'MISSING'}")
    
    # Test model loading
    try:
        reaction_model = joblib.load(os.path.join(models_dir, "reaction_type_model.pkl"))
        print("SUCCESS: Reaction type model loaded successfully")
    except Exception as e:
        print(f"ERROR: Error loading reaction type model: {e}")
    
    try:
        hazard_model = joblib.load(os.path.join(models_dir, "hazard_level_model.pkl"))
        print("SUCCESS: Hazard level model loaded successfully")
    except Exception as e:
        print(f"ERROR: Error loading hazard level model: {e}")

check_ml_models()
```

### Check Dependencies
```python
# check_dependencies.py
import importlib

required_packages = [
    "fastapi",
    "uvicorn",
    "langchain",
    "google.generativeai",
    "pandas",
    "numpy",
    "scikit-learn",
    "rdkit",
    "transformers",
    "torch"
]

print("Checking Dependencies:")
for package in required_packages:
    try:
        importlib.import_module(package)
        print(f"{package}: INSTALLED")
    except ImportError as e:
        print(f"{package}: MISSING - {e}")
```

## Benchmarking

### Run Full Test Suite
```python
# run_full_tests.py
import requests
import time
import json

BASE_URL = "http://localhost:8000"

def run_full_test_suite():
    print("Running ChemPredictAI Test Suite")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {'PASS' if response.status_code == 200 else 'FAIL'}")
    
    # Test 2: ML Prediction
    print("2. Testing ML Prediction...")
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/predict_all", json={
        "reactant1": "ethanol",
        "reactant2": "acetic acid"
    })
    ml_time = time.time() - start_time
    print(f"   Status: {'PASS' if response.status_code == 200 else 'FAIL'}")
    print(f"   Response Time: {ml_time:.2f}s")
    
    # Test 3: LLM Prediction
    print("3. Testing LLM Prediction...")
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/predict_product_llm", json={
        "reactant1": "benzene",
        "reactant2": "nitric acid"
    })
    llm_time = time.time() - start_time
    print(f"   Status: {'PASS' if response.status_code == 200 else 'FAIL'}")
    print(f"   Response Time: {llm_time:.2f}s")
    
    # Test 4: Chat Interface
    print("4. Testing Chat Interface...")
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/chat", json={
        "message": "What is esterification?",
        "session_id": "test123"
    })
    chat_time = time.time() - start_time
    print(f"   Status: {'PASS' if response.status_code == 200 else 'FAIL'}")
    print(f"   Response Time: {chat_time:.2f}s")
    
    print("=" * 50)
    print("Test Suite Complete!")

if __name__ == "__main__":
    run_full_test_suite()
```

## Production Readiness

### Pre-deployment Checklist
- [ ] All ML models load successfully
- [ ] API endpoints respond correctly
- [ ] Response times are acceptable (<5s)
- [ ] Error handling works properly
- [ ] Environment variables are set
- [ ] Dependencies are installed
- [ ] Database connections work
- [ ] Logging is configured

### Performance Targets
- **Response Time**: <5 seconds for predictions
- **Accuracy**: >75% for reaction predictions
- **Uptime**: >99% availability
- **Throughput**: 60 requests/minute

---

**Note**: The ML models work perfectly in local development. The deployment issues are related to build environment compatibility, not the models themselves. You can test all functionality locally while the production deployment is being resolved.