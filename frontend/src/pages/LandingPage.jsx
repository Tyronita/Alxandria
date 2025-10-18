import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { ArrowRight, Sparkles, Brain, Microscope, Shield, MessageSquare, Zap, TrendingUp } from 'lucide-react';

export default function LandingPage() {
  const navigate = useNavigate();

  const researchAreas = [
    {
      icon: <MessageSquare className="w-6 h-6" />,
      title: "NLP & Translation",
      color: "from-purple-500 to-pink-500",
      examples: ["Neural MT", "Multilingual Models", "Low-resource Languages"]
    },
    {
      icon: <Microscope className="w-6 h-6" />,
      title: "Medical AI",
      color: "from-green-500 to-emerald-500",
      examples: ["Disease Classification", "Radiology AI", "Drug Discovery"]
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: "Security & Fraud",
      color: "from-red-500 to-orange-500",
      examples: ["Anomaly Detection", "Transaction Fraud", "Cybersecurity"]
    },
    {
      icon: <Brain className="w-6 h-6" />,
      title: "Computer Vision",
      color: "from-blue-500 to-cyan-500",
      examples: ["Object Detection", "Image Segmentation", "Video Understanding"]
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Reinforcement Learning",
      color: "from-yellow-500 to-amber-500",
      examples: ["Game AI", "Robotics", "Autonomous Systems"]
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: "Time Series & Finance",
      color: "from-indigo-500 to-purple-500",
      examples: ["Stock Prediction", "Forecasting", "Risk Analysis"]
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-xl sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="text-xl font-bold text-gray-900">ResearchAI</span>
              <div className="text-xs text-gray-500">Powered by Perplexity</div>
            </div>
          </div>
          <Button 
            onClick={() => navigate('/research')}
            className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg"
            data-testid="nav-research-btn"
          >
            Start Research
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 pt-20 pb-12">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700 rounded-full text-sm font-medium mb-8 shadow-sm">
            <Sparkles className="w-4 h-4" />
            Interactive Multi-Turn Research Assistant
          </div>
          
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            From Idea to
            <span className="block bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              Research Blueprint
            </span>
          </h1>
          
          <p className="text-lg sm:text-xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">
            Interactive AI assistant that guides you through a conversational journey - from selecting your interests 
            to crafting a cutting-edge ML research proposal with citations and actionable plans.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg"
              onClick={() => navigate('/research')}
              className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-base px-8 py-6 shadow-xl"
              data-testid="hero-start-btn"
            >
              Begin Your Research Journey
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
        </div>
      </section>

      {/* Research Areas Grid */}
      <section className="max-w-7xl mx-auto px-6 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            Explore Cutting-Edge Research Areas
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Choose from curated ML research domains with pre-generated ideas and expert guidance
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {researchAreas.map((area, index) => (
            <Card 
              key={index} 
              className="group p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 bg-white border-2 border-gray-100 cursor-pointer"
              onClick={() => navigate('/research', { state: { selectedArea: area.title } })}
              data-testid={`area-card-${index}`}
            >
              <div className={`w-14 h-14 bg-gradient-to-br ${area.color} rounded-xl flex items-center justify-center text-white mb-4 shadow-lg group-hover:scale-110 transition-transform`}>
                {area.icon}
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                {area.title}
              </h3>
              <div className="flex flex-wrap gap-2">
                {area.examples.map((example, idx) => (
                  <span key={idx} className="text-xs px-3 py-1 bg-gray-100 text-gray-700 rounded-full">
                    {example}
                  </span>
                ))}
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-6 py-16">
        <div className="bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 rounded-3xl p-12 text-white shadow-2xl">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl sm:text-4xl font-bold mb-6">
              How It Works
            </h2>
            <div className="grid md:grid-cols-3 gap-8 mt-12">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
                  1
                </div>
                <h3 className="text-lg font-semibold mb-2">Share Your Interests</h3>
                <p className="text-white/80 text-sm">Tell us about your ML interests, frameworks, and cutting-edge topics you want to explore</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
                  2
                </div>
                <h3 className="text-lg font-semibold mb-2">Conversational Refinement</h3>
                <p className="text-white/80 text-sm">Multi-turn AI chat helps refine your idea with grounded research and expert insights</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold">
                  3
                </div>
                <h3 className="text-lg font-semibold mb-2">Research Blueprint</h3>
                <p className="text-white/80 text-sm">Get a complete research plan with citations, task specs, and actionable next steps</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-gray-50 py-8 mt-16">
        <div className="max-w-7xl mx-auto px-6 text-center text-gray-600">
          <p>Built for Perplexity Hackathon 2025 • Powered by Perplexity AI + Kaggle</p>
        </div>
      </footer>
    </div>
  );
}