# ML Model Setup Guide

This guide will help you set up the ML-based reaction prediction feature.

## ⚠️ Important Note

The ML model requires heavy dependencies (~3GB download):
- PyTorch (~2GB)
- Transformers (ChemBERTa)
- RDKit chemistry toolkit
- RXN4Chemistry API

**The app works perfectly fine without these!** The rule-based prediction is fast and accurate for common reactions.

## 🚀 Quick Start (Rule-Based Only)

If you don't need ML predictions, you're already good to go! The current setup uses:
- ✅ Rule-based predictions (fast, no heavy dependencies)
- ✅ LangChain + Gemini 2.5 Flash for research chat
- ✅ All features working out of the box

## 📦 Installing ML Dependencies

### Step 1: Install Dependencies

```bash
cd ChemPredictAI/backend
source venv/bin/activate

# This will take 10-15 minutes and download ~3GB
pip install -r requirements.txt
```

### Step 2: Set Up RXN4Chemistry (Optional)

RXN4Chemistry requires an API key from IBM:

1. Sign up at: https://rxn.res.ibm.com/
2. Get your API key
3. Set it in your environment:

```bash
export RXN4CHEMISTRY_API_KEY="your_api_key_here"
```

Or add to `.env`:
```
RXN4CHEMISTRY_API_KEY=your_api_key_here
```

### Step 3: Verify Installation

```bash
python -c "import torch; import transformers; from rdkit import Chem; print('✅ All ML packages installed!')"
```

### Step 4: Restart Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
✅ ml model and rxn4chemistry initialized successfully
✅ chempredict ai chatbot initialized successfully with gemini-2.5-flash
```

## 🎯 Using ML Predictions

1. Go to the **Predict** page
2. Toggle the switch to **ML Model**
3. Enter reactant names (e.g., "benzene" and "bromine")
4. Click **Predict**

The ML model will:
- Convert names to SMILES notation
- Predict products using IBM RXN
- Classify reaction type using trained ChemBERTa model
- Predict hazard level

## 📊 What Each Component Does

### Rule-Based Prediction (Default)
- Fast, lightweight
- Pattern-matching based on reactant types
- Good for common reactions
- No internet required

### ML Model Prediction
- Uses IBM RXN API for product prediction
- ChemBERTa transformer for reaction classification
- RDKit for SMILES validation
- More accurate for complex reactions
- Requires internet connection

## ⚙️ Model Files

The trained models are in `ML_Model/models/`:
- `reaction_type_model.pkl` - Random Forest classifier
- `reaction_type_encoder.pkl` - Label encoder
- `hazard_level_model.pkl` - Hazard classifier
- `hazard_level_encoder.pkl` - Hazard label encoder

These use ChemBERTa embeddings for feature extraction.

## 🐛 Troubleshooting

### "ML model not available" error
The backend will automatically fall back to rule-based predictions if ML packages aren't installed.

### RDKit installation fails
Try:
```bash
pip install rdkit-pypi==2022.9.5
```

If that fails, use conda:
```bash
conda install -c conda-forge rdkit
```

### Torch installation is slow
PyTorch is ~2GB. Be patient or install CPU-only version:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### RXN4Chemistry API errors
- Check your API key is set correctly
- Verify your IBM RXN account is active
- Check your rate limits

## 💡 Recommendation

**Start with rule-based predictions** to see if they meet your needs. Only install ML dependencies if you need:
- Product prediction for novel reactions
- SMILES-level accuracy
- Integration with IBM RXN database

The rule-based system is production-ready and works great for educational and demonstration purposes!

