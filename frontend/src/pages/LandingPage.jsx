import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { ArrowRight, Search, BookOpen, Target, Lightbulb, Sparkles, Database, Code } from 'lucide-react';

export default function LandingPage() {
  const navigate = useNavigate();

  const features = [
    {
      icon: <Search className="w-6 h-6" />,
      title: "Intelligent Research",
      description: "Transform curiosity into structured research with AI-powered insights"
    },
    {
      icon: <BookOpen className="w-6 h-6" />,
      title: "SOTA Reviews",
      description: "Access academic literature and cutting-edge research findings"
    },
    {
      icon: <Target className="w-6 h-6" />,
      title: "Task Specifications",
      description: "Generate precise, actionable task specs with metrics and constraints"
    },
    {
      icon: <Lightbulb className="w-6 h-6" />,
      title: "Technique Discovery",
      description: "Find proven techniques from Kaggle, GitHub, and research papers"
    },
    {
      icon: <Database className="w-6 h-6" />,
      title: "Kaggle Integration",
      description: "Explore datasets and competitions directly from the platform"
    },
    {
      icon: <Code className="w-6 h-6" />,
      title: "Evidence-Based",
      description: "Every recommendation backed by citations and real-world examples"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 via-white to-blue-50">
      {/* Header */}
      <header className="border-b bg-white/70 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">ResearchAI</span>
          </div>
          <Button 
            onClick={() => navigate('/research')}
            className="bg-blue-600 hover:bg-blue-700"
            data-testid="nav-research-btn"
          >
            Start Research
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 pt-20 pb-16">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium mb-8">
            <Sparkles className="w-4 h-4" />
            Powered by Perplexity AI
          </div>
          
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            From Curiosity to
            <span className="block bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
              Research Excellence
            </span>
          </h1>
          
          <p className="text-lg sm:text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            AI-powered research assistant that transforms your ideas into structured research, 
            complete with citations, task specs, and actionable recommendations.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg"
              onClick={() => navigate('/research')}
              className="bg-blue-600 hover:bg-blue-700 text-base px-8 py-6"
              data-testid="hero-start-btn"
            >
              Start Research
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
            <Button 
              size="lg"
              variant="outline"
              className="border-2 border-gray-300 hover:border-blue-500 hover:bg-blue-50 text-base px-8 py-6"
              data-testid="learn-more-btn"
            >
              Learn More
            </Button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            Everything You Need for Research
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Comprehensive research toolkit powered by Perplexity's advanced AI and real-time web search
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 bg-white border-gray-200"
              data-testid={`feature-card-${index}`}
            >
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600 mb-4">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </Card>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <Card className="bg-gradient-to-br from-blue-600 to-cyan-500 p-12 text-center text-white border-0">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            Ready to Transform Your Research?
          </h2>
          <p className="text-xl mb-8 text-blue-100 max-w-2xl mx-auto">
            Start exploring with AI-powered insights, citations, and recommendations
          </p>
          <Button 
            size="lg"
            onClick={() => navigate('/research')}
            className="bg-white text-blue-600 hover:bg-gray-50 text-base px-8 py-6"
            data-testid="cta-start-btn"
          >
            Get Started Now
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
        </Card>
      </section>

      {/* Footer */}
      <footer className="border-t bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center text-gray-600">
          <p>Built for Perplexity Hackathon 2025 • Powered by Perplexity AI + Kaggle</p>
        </div>
      </footer>
    </div>
  );
}