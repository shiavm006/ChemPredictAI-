#!/usr/bin/env python3

print("Testing ML model loading...")

try:
    print("1. Testing basic imports...")
    import joblib
    import numpy as np
    print("✓ Basic imports successful")
    
    print("2. Testing model file loading...")
    downloads_folder = "/Users/shivammittal/Downloads"
    models_dir = f"{downloads_folder}/TrainedData"
    
    clf_type = joblib.load(f"{models_dir}/reaction_type_model.pkl")
    le_type = joblib.load(f"{models_dir}/reaction_type_encoder.pkl")
    clf_hazard = joblib.load(f"{models_dir}/hazard_level_model.pkl")
    le_hazard = joblib.load(f"{models_dir}/hazard_level_encoder.pkl")
    print("✓ Model files loaded successfully")
    
    print("3. Testing ChemBERTa import...")
    from transformers import AutoTokenizer, AutoModel
    print("✓ Transformers import successful")
    
    print("4. Testing ChemBERTa model loading...")
    tokenizer = AutoTokenizer.from_pretrained("seyonec/ChemBERTa-zinc-base-v1")
    model = AutoModel.from_pretrained("seyonec/ChemBERTa-zinc-base-v1")
    print("✓ ChemBERTa model loaded successfully")
    
    print("5. Testing feature extraction...")
    test_smiles = "CCO"
    inputs = tokenizer(test_smiles, return_tensors="pt")
    import torch
    with torch.no_grad():
        outputs = model(**inputs)
        features = outputs.last_hidden_state.mean(dim=1).squeeze()
    print("✓ Feature extraction successful")
    print(f"Features shape: {features.shape}")
    
    print("\nAll tests passed! ML models are working correctly.")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

