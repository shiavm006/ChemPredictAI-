# ChemPredict AI

A full-stack chemical reaction prediction application built with FastAPI and React.

## Features

- **AI-Powered Predictions**: Advanced machine learning algorithms for chemical reaction analysis
- **3D Visualization**: Interactive WebGL orb with hover effects
- **Research Chat**: AI-powered research assistant for chemical analysis
- **Modern UI**: Minimalist design with glassmorphism effects
- **Real-Time Analysis**: Instant predictions for chemical reactions

## Tech Stack

### Backend
- FastAPI with Python 3.13
- CORS support for frontend integration
- Pydantic for data validation

### Frontend
- React 18 with TypeScript
- Vite for fast development
- Tailwind CSS for styling
- WebGL for 3D graphics
- shadcn/ui components

## Getting Started

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `GET /` - Health check
- `POST /predict` - Predict chemical reaction between two reactants

## Project Structure

```
├── backend/
│   ├── main.py          # FastAPI application
│   └── venv/           # Python virtual environment
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── lib/        # Utility functions
│   │   └── App.tsx     # Main application
│   ├── package.json    # Dependencies
│   └── vite.config.ts  # Vite configuration
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

© 2024 ChemPredict AI. All rights reserved.
