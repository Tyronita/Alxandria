import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';

export default function LandingPage() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');

  const handleStart = () => {
    if (query.trim()) {
      navigate('/research', { state: { initialQuery: query } });
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center px-6">
      {/* Logo */}
      <div className="mb-12">
        <img 
          src="/alexandria-logo.png" 
          alt="Alexandria" 
          className="h-20 w-auto"
        />
      </div>

      {/* Main Input */}
      <div className="max-w-2xl w-full">
        <Input
          placeholder="What research topic are you curious about?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleStart()}
          className="h-14 text-lg border-2 border-gray-300 focus:border-blue-500 rounded-lg mb-4"
          data-testid="main-input"
        />
        <Button
          onClick={handleStart}
          disabled={!query.trim()}
          size="lg"
          className="w-full h-14 bg-blue-600 hover:bg-blue-700 text-lg"
          data-testid="start-btn"
        >
          Start Research
          <ArrowRight className="w-5 h-5 ml-2" />
        </Button>
      </div>

      {/* Powered by */}
      <div className="mt-12 flex items-center gap-3 text-sm text-gray-500">
        <span>Powered by</span>
        <img 
          src="/perplexity-logo.png" 
          alt="Perplexity" 
          className="h-5 w-auto"
        />
      </div>
    </div>
  );
}