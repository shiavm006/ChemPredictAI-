# ChemPredict AI

AI-powered chemical reaction predictor with ML models and Gemini-powered research assistant.

## Features

- **Reaction Prediction**: Predict reaction type, hazard level, and products using ML models
- **Safety Assessment**: Analyze safety hazards of chemical reactions
- **Research Chat**: AI-powered chatbot for chemistry questions using Gemini
- **SMILES Conversion**: Automatic conversion between chemical names and SMILES notation

## Tech Stack

- **Backend**: FastAPI, Python 3.11
- **ML Models**: Scikit-learn, ChemBERTa, RXN4Chemistry
- **AI**: Google Gemini (LangChain)
- **Frontend**: React, TypeScript, Vite, TailwindCSS

## Environment Variables

Create a `.env` file in the backend directory:

```env
GOOGLE_API_KEY=your_gemini_api_key
RXN4CHEMISTRY_API_KEY=your_rxn_api_key
```

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## ML Models

The ML models are stored separately due to their size. They are automatically loaded at startup.

## License

MIT License

