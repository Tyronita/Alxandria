import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { ArrowRight, Sparkles, Search, Lightbulb, TrendingUp } from 'lucide-react';
import { useState } from 'react';

export default function LandingPage() {
  const navigate = useNavigate();
  const [curiosity, setCuriosity] = useState('');

  const handleStart = () => {
    if (curiosity.trim()) {
      navigate('/research', { state: { initialQuery: curiosity } });
    } else {
      navigate('/research');
    }
  };

  const exampleTopics = [
    { icon: '🧬', text: 'How AI is revolutionizing drug discovery', color: 'from-green-400 to-emerald-600' },
    { icon: '🤖', text: 'The future of large language models', color: 'from-blue-400 to-indigo-600' },
    { icon: '🎨', text: 'Generative AI and creative applications', color: 'from-purple-400 to-pink-600' },
    { icon: '🔒', text: 'AI for cybersecurity and fraud detection', color: 'from-red-400 to-orange-600' },
    { icon: '🚗', text: 'Self-driving cars and computer vision', color: 'from-cyan-400 to-blue-600' },
    { icon: '💬', text: 'Natural language processing breakthroughs', color: 'from-violet-400 to-purple-600' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-xl sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="text-xl font-bold text-gray-900">ResearchAI</span>
              <div className="text-xs text-gray-500">Your AI Research Guide</div>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-5xl mx-auto px-6 pt-24 pb-16">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium mb-6 shadow-sm">
            <Sparkles className="w-4 h-4" />
            Powered by Perplexity AI
          </div>
          
          <h1 className="text-6xl sm:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            What do you want to
            <span className="block bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
              learn about?
            </span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
            Start with your curiosity. I'll guide you through cutting-edge research, 
            explain the concepts, and help you discover novel ideas.
          </p>

          {/* Main Input */}
          <div className="max-w-3xl mx-auto mb-8">
            <div className="flex gap-3">
              <div className="flex-1 relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <Input
                  placeholder="e.g., using AI to detect diseases early, building better recommendation systems..."
                  value={curiosity}
                  onChange={(e) => setCuriosity(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleStart()}
                  className="h-16 pl-12 pr-4 text-lg border-2 border-gray-200 focus:border-blue-500 rounded-2xl shadow-lg"
                  data-testid="curiosity-input"
                />
              </div>
              <Button
                onClick={handleStart}
                size="lg"
                className="h-16 px-8 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 rounded-2xl shadow-lg text-lg"
                data-testid="start-journey-btn"
              >
                Start Journey
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </div>
        </div>

        {/* Example Topics */}
        <div className="max-w-4xl mx-auto">
          <p className="text-center text-sm text-gray-500 mb-6 flex items-center justify-center gap-2">
            <Lightbulb className="w-4 h-4" />
            Or explore these trending topics
          </p>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {exampleTopics.map((topic, idx) => (
              <Card
                key={idx}
                onClick={() => {
                  setCuriosity(topic.text);
                  navigate('/research', { state: { initialQuery: topic.text } });
                }}
                className="p-4 cursor-pointer hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border-2 border-gray-100 hover:border-blue-300 group"
                data-testid={`example-${idx}`}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 bg-gradient-to-br ${topic.color} rounded-xl flex items-center justify-center text-2xl shadow-md group-hover:scale-110 transition-transform`}>
                    {topic.icon}
                  </div>
                  <p className="text-sm font-medium text-gray-700 group-hover:text-gray-900 flex-1">
                    {topic.text}
                  </p>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="max-w-6xl mx-auto px-6 py-16">
        <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-3xl p-12 text-white shadow-2xl">
          <h2 className="text-3xl font-bold mb-4 text-center">How Your Research Journey Works</h2>
          <p className="text-center text-blue-100 mb-12 max-w-2xl mx-auto">
            A guided conversation that takes you from curiosity to actionable research idea
          </p>
          
          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mx-auto mb-4 text-3xl">
                💭
              </div>
              <h3 className="font-semibold mb-2">Share Curiosity</h3>
              <p className="text-sm text-blue-100">Tell me what fascinates you</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mx-auto mb-4 text-3xl">
                🔍
              </div>
              <h3 className="font-semibold mb-2">Explore Research</h3>
              <p className="text-sm text-blue-100">See cutting-edge work with citations</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mx-auto mb-4 text-3xl">
                🚀
              </div>
              <h3 className="font-semibold mb-2">Discover Ideas</h3>
              <p className="text-sm text-blue-100">Find novel directions & gaps</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mx-auto mb-4 text-3xl">
                🎯
              </div>
              <h3 className="font-semibold mb-2">Build Plan</h3>
              <p className="text-sm text-blue-100">Get actionable next steps</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white/80 py-8 mt-16">
        <div className="max-w-7xl mx-auto px-6 text-center text-gray-600">
          <p>Built for Perplexity Hackathon 2025 • Powered by Perplexity AI</p>
        </div>
      </footer>
    </div>
  );
}