import React from "react";
import { cn } from "@/lib/utils";

const cardContents = [
  {
    title: "AI-Powered Predictions",
    description:
      "Advanced machine learning algorithms analyze chemical structures and predict reaction outcomes with high accuracy. Our AI models are trained on vast databases of chemical reactions.",
  },
  {
    title: "Real-Time Analysis",
    description:
      "Get instant predictions for chemical reactions as you input reactants. No waiting time - receive comprehensive analysis including reaction type and yield predictions in seconds.",
  },
  {
    title: "Comprehensive Database",
    description:
      "Access extensive chemical databases covering organic, inorganic, and biochemical reactions. From simple substitutions to complex multi-step syntheses, our platform covers reactions across all chemical domains.",
  },  
  {
    title: "Interactive 3D Visualization",
    description:
      "Experience chemical structures and reactions through stunning 3D visualizations. Our WebGL-powered interface provides an immersive way to understand molecular interactions.",
  },
  {
    title: "Research-Grade Accuracy",
    description:
      "Built for chemists, by chemists. Our predictions are validated against experimental data and peer-reviewed research, ensuring reliable results for laboratory applications.",
  },
];

const PlusCard: React.FC<{
  className?: string;
  title: string;
  description: string;
}> = ({ className = "", title, description }) => {
  return (
    <div
      className={cn(
        "relative border border-dashed border-gray-600 dark:border-gray-400 rounded-lg p-6 bg-gray-900/20 dark:bg-gray-800/20 backdrop-blur-sm min-h-[200px]",
        "flex flex-col justify-between hover:bg-gray-800/30 transition-all duration-300",
        className
      )}
    >
      <CornerPlusIcons />
      {/* Content */}
      <div className="relative z-10 space-y-2">
        <h3 className="text-xl font-bold text-white">
          {title}
        </h3>
        <p className="text-gray-300">{description}</p>
      </div>
    </div>
  );
};

const CornerPlusIcons = () => (
  <>
    <PlusIcon className="absolute -top-3 -left-3" />
    <PlusIcon className="absolute -top-3 -right-3" />
    <PlusIcon className="absolute -bottom-3 -left-3" />
    <PlusIcon className="absolute -bottom-3 -right-3" />
  </>
);

const PlusIcon = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    width={24}
    height={24}
    strokeWidth="1"
    stroke="currentColor"
    className={`text-purple-400 size-6 ${className}`}
  >
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m6-6H6" />
  </svg>
);

export default function FeaturesBentoCards() {
  return (
    <section className="bg-black">
      <div className="mx-auto container py-20 px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-6">
            Powerful Features
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Discover the cutting-edge capabilities that make ChemPredict AI the ultimate tool for chemical research and analysis.
          </p>
        </div>

        {/* Responsive Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 auto-rows-auto gap-4 mb-16">
          <PlusCard {...cardContents[0]} className="lg:col-span-3 lg:row-span-2" />
          <PlusCard {...cardContents[1]} className="lg:col-span-2 lg:row-span-2" />
          <PlusCard {...cardContents[2]} className="lg:col-span-4 lg:row-span-1" />
          <PlusCard {...cardContents[3]} className="lg:col-span-2 lg:row-span-1" />
          <PlusCard {...cardContents[4]} className="lg:col-span-2 lg:row-span-1" />
        </div>

        {/* Section Footer */}
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-3xl md:text-5xl font-bold text-white mb-6">
            Built for chemists. Designed for innovation.
          </h3>
          <p className="text-gray-400 text-lg leading-relaxed">
            ChemPredict AI combines the power of artificial intelligence with deep chemical knowledge to revolutionize how we understand and predict chemical reactions. From academic research to industrial applications, our platform provides the tools you need to accelerate discovery.
          </p>
        </div>
      </div>
    </section>
  );
}
