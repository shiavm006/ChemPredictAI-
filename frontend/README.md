# ChemPredict AI Frontend

A modern React frontend for chemical reaction prediction using artificial intelligence.

## Features

- **Chemical Reaction Prediction**: Input two reactants and get AI-powered predictions
- **Modern UI**: Built with React, TypeScript, and Tailwind CSS
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Predictions**: Fast API integration for instant results

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **shadcn/ui** components with Radix UI primitives
- **React Hook Form** for form handling

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open your browser and visit `http://localhost:8080`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Backend Integration

This frontend connects to a FastAPI backend running on `http://127.0.0.1:8000`. Make sure the backend is running before using the application.

## API Endpoints

- `POST /predict` - Predict chemical reaction between two reactants

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── lib/           # Utility functions
├── hooks/         # Custom React hooks
├── App.tsx        # Main application component
└── main.tsx       # Application entry point
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the ChemPredict AI system.