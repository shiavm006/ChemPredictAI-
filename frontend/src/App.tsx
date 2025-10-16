import { useState } from "react";
import Orb from "./components/Orb";
import Header from "./components/Header";
import FeaturesBentoCards from "./components/FeaturesBentoCards";
import ChemPredictChat from "./components/ChemPredictChat";
import Footer from "./components/Footer";
import { TestimonialsSection } from "./components/TestimonialsSection";
import { Brain, Droplets, Zap, Download, History } from "lucide-react";

interface ReactionResult {
  reaction_type: string;
  product: string;
  safety_hazard_level: string;
  reaction_description: string;
  predicted_yield: string;
}

interface PredictionHistory {
  id: string;
  compound: string;
  reaction_type: string;
  yield: string;
  timestamp: Date;
}

function App() {
  const [activeTab, setActiveTab] = useState<string>("home");
  const [r1, setR1] = useState<string>("");
  const [r2, setR2] = useState<string>("");
  const [result, setResult] = useState<ReactionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [predictionHistory, setPredictionHistory] = useState<PredictionHistory[]>([]);
  const [useMLModel, setUseMLModel] = useState<boolean>(false);
  const [mlModelAvailable, setMlModelAvailable] = useState<boolean>(false);

  // Common compounds for autocomplete
  const commonCompounds = [
    "H2O", "NaCl", "CO2", "CH4", "C6H12O6", "H2SO4", "NaOH", "HCl", 
    "NH3", "CaCO3", "C2H5OH", "CH3COOH", "Water", "Sodium Chloride",
    "Carbon Dioxide", "Methane", "Glucose", "Sulfuric Acid", "Sodium Hydroxide"
  ];

  // Testimonials data
  const testimonials = [
    {
      author: {
        name: "Dr. Sarah Chen",
        handle: "Professor of Chemistry, MIT",
        avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&h=150&fit=crop&crop=face"
      },
      text: "ChemPredict AI has revolutionized our research methodology. The accuracy of reaction predictions has significantly accelerated our drug discovery projects."
    },
    {
      author: {
        name: "Prof. Michael Rodriguez",
        handle: "Organic Chemistry, Stanford",
        avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face"
      },
      text: "The AI's ability to predict reaction yields and safety hazards has saved us countless hours in lab planning. It's become an essential tool in our research."
    },
    {
      author: {
        name: "Dr. Emily Watson",
        handle: "Chemical Engineering, Caltech",
        avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&h=150&fit=crop&crop=face"
      },
      text: "As an industry expert, I can confidently say ChemPredict AI delivers results that match our most sophisticated computational models."
    },
    {
      author: {
        name: "Prof. James Thompson",
        handle: "Materials Science, Oxford",
        avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face"
      },
      text: "The platform's intuitive interface combined with its powerful prediction capabilities makes it accessible to both students and seasoned researchers."
    },
    {
      author: {
        name: "Dr. Lisa Park",
        handle: "Pharmaceutical Sciences, Harvard",
        avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face"
      },
      text: "ChemPredict AI has transformed how we approach synthetic chemistry. The safety hazard predictions have prevented several potential accidents in our lab."
    },
    {
      author: {
        name: "Prof. David Kumar",
        handle: "Chemistry, Cambridge",
        avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face"
      },
      text: "The accuracy of reaction type predictions is remarkable. It's like having a world-class chemist available 24/7 for consultation."
    }
  ];

  const handlePredict = async () => {
    if (!r1 || !r2) {
      setError("Please enter both reactants.");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      // choose endpoint based on ml model toggle
      const endpoint = useMLModel ? "http://127.0.0.1:8000/predict_all" : "http://127.0.0.1:8000/predict";
      
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reactant1: r1, reactant2: r2 }),
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Server error: ${res.status} - ${errorText}`);
      }

      const data: ReactionResult = await res.json();
      setResult(data);
      
      // Add to history
      const historyEntry: PredictionHistory = {
        id: Date.now().toString(),
        compound: `${r1} + ${r2}`,
        reaction_type: data.reaction_type,
        yield: data.predicted_yield,
        timestamp: new Date()
      };
      setPredictionHistory(prev => [historyEntry, ...prev.slice(0, 4)]);
      
    } catch (err: any) {
      console.error(err);
      if (err.message.includes('fetch')) {
        setError("Cannot connect to backend. Please ensure the server is running on http://127.0.0.1:8000");
      } else {
        setError(`Error: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const getSafetyColor = (level: string) => {
    const levelLower = level.toLowerCase();
    if (levelLower === 'low') return 'text-green-400';
    if (levelLower === 'medium') return 'text-yellow-400';
    if (levelLower === 'high') return 'text-red-400';
    return 'text-gray-400';
  };

  const handleHistoryClick = (entry: PredictionHistory) => {
    // Parse the compound string to extract reactants
    const parts = entry.compound.split(' + ');
    if (parts.length === 2) {
      setR1(parts[0].trim());
      setR2(parts[1].trim());
      // Auto-trigger prediction
      setTimeout(() => {
        handlePredict();
      }, 100);
    }
  };

  const generateReport = (result: ReactionResult, reactant1: string, reactant2: string) => {
    const reportContent = `
CHEMPREDICT AI - REACTION ANALYSIS REPORT
==========================================

Generated on: ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}

REACTION DETAILS
----------------
Reactants: ${reactant1} + ${reactant2}
Product: ${result.product}
Reaction Type: ${result.reaction_type}
Predicted Yield: ${result.predicted_yield}
Safety Hazard Level: ${result.safety_hazard_level}

REACTION DESCRIPTION
-------------------
${result.reaction_description}

SAFETY CONSIDERATIONS
--------------------
Hazard Level: ${result.safety_hazard_level}
${result.safety_hazard_level === 'Low' ? '• Generally safe reaction with minimal precautions needed' : 
  result.safety_hazard_level === 'Medium' ? '• Moderate safety precautions required - monitor temperature and pressure' : 
  '• High safety precautions required - use proper protective equipment and controlled environment'}

PREDICTION CONFIDENCE
--------------------
Yield Range: ${result.predicted_yield}
Reaction Type Confidence: High
Safety Assessment: Based on standard chemical databases

DISCLAIMER
----------
This report is generated using ChemPredict AI for educational and research purposes. 
Always consult with qualified chemists and follow proper laboratory safety protocols 
before conducting any chemical reactions. Actual results may vary based on conditions 
and experimental setup.

---
Generated by ChemPredict AI
© 2024 ChemPredict AI. All rights reserved.
    `;

    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ChemPredict_Report_${reactant1}_${reactant2}_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };


  const renderHomeView = () => (
    <>
      <div className="relative h-screen flex items-center justify-center">
        {/* Background Orb */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div style={{ width: '100%', height: '600px', position: 'relative' }}>
            <Orb
              hoverIntensity={0.5}
              rotateOnHover={true}
              hue={0}
              forceHoverState={false}
            />
          </div>
        </div>

        {/* Content Overlay */}
        <div className="relative z-10 text-center px-8 max-w-4xl">
          <h1 className="text-5xl md:text-7xl font-light mb-8 text-white tracking-tight">
            ChemPredict AI
          </h1>
          <p className="text-lg md:text-xl mb-12 text-gray-400 max-w-2xl mx-auto font-light leading-relaxed">
            Predict chemical reactions with cutting-edge artificial intelligence
          </p>
          <button 
            onClick={() => setActiveTab('predict')}
            className="px-6 py-3 rounded-lg border border-white/20 bg-white/5 backdrop-blur-sm text-white hover:bg-white/10 hover:border-white/30 transition-all duration-300 text-sm font-medium"
          >
            Start Predicting →
          </button>
        </div>
      </div>

      {/* Features Section */}
      <FeaturesBentoCards />

      {/* Testimonials Section */}
      <TestimonialsSection
        title="Trusted by leading researchers worldwide"
        description="Join thousands of chemists, researchers, and industry experts who rely on ChemPredict AI for accurate reaction predictions"
        testimonials={testimonials}
      />
    </>
  );

  const renderPredictView = () => (
    <div className="relative z-10 bg-black min-h-screen py-20">
      <div className="flex gap-8">
        {/* Sidebar */}
        {predictionHistory.length > 0 && (
          <div className="w-80 p-6 ml-4 border-r border-gray-800">
            <h3 className="text-white text-base font-medium mb-6 pb-3 border-b border-gray-800 text-center">Recent Reactions</h3>
            
            <div className="space-y-3">
              {predictionHistory.map((entry) => (
                <div 
                  key={entry.id} 
                  onClick={() => handleHistoryClick(entry)}
                  className="p-3 hover:bg-gray-900/30 transition-colors cursor-pointer rounded"
                >
                  <div className="space-y-1">
                    <p className="text-white text-sm font-light">{entry.compound}</p>
                    <div className="flex items-center justify-between">
                      <p className="text-gray-400 text-xs">
                        {entry.reaction_type}
                      </p>
                      <p className="text-gray-500 text-xs">
                        {entry.yield}
                      </p>
                    </div>
                    <p className="text-gray-600 text-xs">
                      {entry.timestamp.toLocaleDateString()} {entry.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="flex-1 max-w-4xl mx-auto px-8">
        {/* Header Section */}
        <div className="text-center mb-20">
          <h1 className="text-4xl font-light text-white tracking-tight mb-4">
            Chemical Reaction Predictor
          </h1>
          <p className="text-gray-500 max-w-2xl mx-auto font-light">
            Enter two chemical reactants to predict their reaction
          </p>
        </div>

                {/* Input Section */}
                <div className="max-w-xl mx-auto mb-16">
                  {/* ml model toggle */}
                  <div className="mb-6 flex items-center justify-center gap-3">
                    <span className="text-gray-400 text-sm">Rule-based</span>
                    <button
                      onClick={() => setUseMLModel(!useMLModel)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        useMLModel ? 'bg-purple-600' : 'bg-gray-700'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          useMLModel ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                    <span className="text-gray-400 text-sm">ML Model</span>
                    {useMLModel && (
                      <span className="text-xs text-purple-400 ml-2">
                        (requires heavy dependencies)
                      </span>
                    )}
                  </div>

                  <div className="space-y-4">
                    <input
                      type="text"
                      value={r1}
                      onChange={(e) => setR1(e.target.value)}
                      placeholder="Reactant 1"
                      className="w-full p-4 rounded-lg bg-gray-900/50 border border-gray-800 focus:border-white/20 focus:outline-none text-white placeholder-gray-500 text-sm"
                      list="compounds"
                    />
                    <input
                      type="text"
                      value={r2}
                      onChange={(e) => setR2(e.target.value)}
                      placeholder="Reactant 2"
                      className="w-full p-4 rounded-lg bg-gray-900/50 border border-gray-800 focus:border-white/20 focus:outline-none text-white placeholder-gray-500 text-sm"
                      list="compounds"
                    />
                    <datalist id="compounds">
                      {commonCompounds.map((compound) => (
                        <option key={compound} value={compound} />
                      ))}
                    </datalist>
                  </div>
          
          <button
            onClick={handlePredict}
            disabled={loading || !r1.trim() || !r2.trim()}
            className={`w-full mt-6 py-3 rounded-lg font-light text-sm transition-all duration-300 ${
              loading || !r1.trim() || !r2.trim()
                ? "bg-gray-800 cursor-not-allowed text-gray-600" 
                : "bg-white text-black hover:bg-gray-200"
            }`}
          >
            {loading ? "Predicting..." : "Predict"}
          </button>

          {error && (
            <div className="mt-4 p-3 bg-red-900/30 border border-red-800/50 rounded-lg">
              <p className="text-red-400 text-center text-sm">{error}</p>
            </div>
          )}
        </div>

        {/* Results Section */}
        {result && (
          <div className="max-w-4xl mx-auto mb-16">
            <div className="text-center mb-8 relative">
              <p className="text-gray-500 text-sm mb-6">
                {r1} + {r2}
              </p>
              {/* Generate Report Icon */}
              <button
                onClick={() => generateReport(result, r1, r2)}
                className="absolute top-0 right-0 p-2 text-gray-400 hover:text-white transition-colors"
                title="Generate Report"
              >
                <Download className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              {/* Product */}
              <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-800">
                <p className="text-gray-500 text-xs mb-2">Product</p>
                <p className="text-white text-sm font-light">
                  {result.product}
                </p>
              </div>

              {/* Reaction Type */}
              <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-800">
                <p className="text-gray-500 text-xs mb-2">Reaction Type</p>
                <p className="text-white text-sm font-light">
                  {result.reaction_type}
                </p>
              </div>

              {/* Safety Hazard Level */}
              <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-800">
                <p className="text-gray-500 text-xs mb-2">Safety Level</p>
                <p className={`text-sm font-light ${getSafetyColor(result.safety_hazard_level)}`}>
                  {result.safety_hazard_level}
                </p>
              </div>

              {/* Predicted Yield */}
              <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-800">
                <p className="text-gray-500 text-xs mb-2">Predicted Yield</p>
                <p className="text-white text-sm font-light">
                  {result.predicted_yield}
                </p>
              </div>
            </div>

            {/* Reaction Description */}
            <div className="bg-gray-900/30 p-6 rounded-lg border border-gray-800">
              <p className="text-gray-500 text-xs mb-3">Reaction Description</p>
              <p className="text-gray-300 text-sm font-light leading-relaxed">
                {result.reaction_description}
              </p>
            </div>
          </div>
        )}

        </div>
      </div>
    </div>
  );

  const renderResearchChatView = () => (
    <ChemPredictChat />
  );

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Header */}
      <Header activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Main Content */}
      <main className="pt-20">
        {activeTab === 'home' && renderHomeView()}
        {activeTab === 'predict' && renderPredictView()}
        {activeTab === 'research' && renderResearchChatView()}
      </main>

      {/* Footer */}
      {activeTab === 'home' && <Footer />}
    </div>
  );
}

export default App;