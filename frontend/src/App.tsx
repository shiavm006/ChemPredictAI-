import { useState } from "react";
import Orb from "./components/Orb";
import Header from "./components/Header";
import FeaturesBentoCards from "./components/FeaturesBentoCards";
import ChemPredictChat from "./components/ChemPredictChat";

interface ReactionResult {
  reaction_type: string;
  predicted_yield: string;
}

function App() {
  const [activeTab, setActiveTab] = useState<string>("home");
  const [r1, setR1] = useState<string>("");
  const [r2, setR2] = useState<string>("");
  const [result, setResult] = useState<ReactionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const handlePredict = async () => {
    if (!r1 || !r2) {
      setError("Please enter both reactants.");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
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
    </>
  );

  const renderPredictView = () => (
    <div className="relative z-10 bg-gray-900/50 backdrop-blur-sm py-20 px-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
            Chemical Reaction Predictor
          </h2>
          
          <div className="bg-gray-800/50 backdrop-blur-sm p-8 rounded-3xl border border-gray-700/50">
            <div className="grid md:grid-cols-2 gap-8">
              <div className="space-y-4">
                <input
                  className="w-full p-4 rounded-xl bg-gray-700/50 border border-gray-600 focus:border-purple-500 focus:outline-none text-white placeholder-gray-400"
                  placeholder="Enter Reactant 1"
                  value={r1}
                  onChange={(e) => setR1(e.target.value)}
                />
                <input
                  className="w-full p-4 rounded-xl bg-gray-700/50 border border-gray-600 focus:border-purple-500 focus:outline-none text-white placeholder-gray-400"
                  placeholder="Enter Reactant 2"
                  value={r2}
                  onChange={(e) => setR2(e.target.value)}
                />
                <button
                  onClick={handlePredict}
                  className={`w-full py-4 rounded-xl font-semibold text-lg transition-all duration-300 ${
                    loading 
                      ? "bg-gray-600 cursor-not-allowed" 
                      : "bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 transform hover:scale-105"
                  }`}
                  disabled={loading}
                >
                  {loading ? "Predicting..." : "Predict Reaction"}
                </button>
              </div>

              <div className="flex items-center justify-center">
                {error && (
                  <div className="text-red-400 text-center">
                    <p className="text-lg font-semibold">{error}</p>
                  </div>
                )}

                {result && (
                  <div className="text-center space-y-4">
                    <div className="bg-gradient-to-r from-purple-500/20 to-blue-500/20 p-6 rounded-2xl border border-purple-500/30">
                      <p className="text-lg font-semibold text-gray-300 mb-2">
                        Reaction Type:
                      </p>
                      <p className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                        {result.reaction_type}
                      </p>
                    </div>
                    <div className="bg-gradient-to-r from-purple-500/20 to-blue-500/20 p-6 rounded-2xl border border-purple-500/30">
                      <p className="text-lg font-semibold text-gray-300 mb-2">
                        Predicted Yield:
                      </p>
                      <p className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                        {result.predicted_yield}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
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
      {activeTab !== 'research' && (
        <footer className="relative z-10 text-center py-8 text-gray-400 border-t border-gray-800">
          <p>© 2024 ChemPredict AI. All rights reserved.</p>
        </footer>
      )}
    </div>
  );
}

export default App;