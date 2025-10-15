interface HeaderProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export default function Header({ activeTab, onTabChange }: HeaderProps) {
  const tabs = [
    { id: 'home', label: 'Home' },
    { id: 'predict', label: 'Predict' },
    { id: 'research', label: 'Research' }
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-black/40 backdrop-blur-xl border-b border-white/5">
      <div className="w-full py-6">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center pl-8">
            <span className="text-white font-light text-lg tracking-wide">ChemPredict AI</span>
          </div>

          {/* Navigation Tabs - Moved to the right */}
          <nav className="flex items-center space-x-8 pr-[68px]">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`text-sm font-light transition-all duration-300 relative ${
                  activeTab === tab.id
                    ? 'text-white'
                    : 'text-gray-500 hover:text-gray-300'
                }`}
              >
                {tab.label}
                {activeTab === tab.id && (
                  <div className="absolute -bottom-2 left-0 right-0 h-px bg-white"></div>
                )}
              </button>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
}
