# Local Testing

ML models work locally but having deployment issues. Test them here.

**Dataset:** [Google Drive Link](https://drive.google.com/drive/folders/1frpLZMOvq0Vh7FrUdwUDVY-VYli8xpuD?usp=sharing)

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# add your keys to .env
echo "GOOGLE_API_KEY=your_key" > .env

# run backend
uvicorn main:app --reload
```

## Test ML models

```python
# test ml prediction
from ML_Model.predict.predict_reaction import predict_reaction

result = predict_reaction("ethanol", "acetic acid", input_type="name")
print(result)
```

## Test API

```python
import requests

# test prediction
response = requests.post("http://localhost:8000/predict_all", json={
    "reactant1": "benzene",
    "reactant2": "nitric acid"
})
print(response.json())
```

## Test individual models

```python
import joblib

# load models
reaction_model = joblib.load('ML_Model/models/reaction_type_model.pkl')
hazard_model = joblib.load('ML_Model/models/hazard_level_model.pkl')

# test prediction
# ... your test code here
```

## Quick tests

```python
# test response time
import time
start = time.time()
# ... your test code
print(f"Response time: {time.time() - start:.2f}s")
```

## Test some reactions

```python
# test a few common reactions
reactions = [
    ("ethanol", "acetic acid"),
    ("benzene", "nitric acid"),
    ("methanol", "formic acid")
]

for r1, r2 in reactions:
    response = requests.post("http://localhost:8000/predict_all", json={
        "reactant1": r1, "reactant2": r2
    })
    print(f"{r1} + {r2} → {response.json()['product']}")
```

## Debug

```python
# check if models exist
import os
models_dir = "ML_Model/models"
files = ["reaction_type_model.pkl", "hazard_level_model.pkl"]
for f in files:
    print(f"{f}: {'EXISTS' if os.path.exists(os.path.join(models_dir, f)) else 'MISSING'}")
```

That's it! The ML models work locally, just having deployment issues with the chemistry libraries.