import React, { useState, useEffect } from 'react';
import { Search, Database, Brain, CheckCircle2, Loader2 } from 'lucide-react';
import { Card } from '@/components/ui/card';

const steps = [
  { icon: Search, text: 'Searching literature', color: 'text-blue-600', bg: 'bg-blue-100' },
  { icon: Database, text: 'Finding datasets', color: 'text-green-600', bg: 'bg-green-100' },
  { icon: Brain, text: 'Analyzing methods', color: 'text-purple-600', bg: 'bg-purple-100' },
  { icon: CheckCircle2, text: 'Synthesizing insights', color: 'text-indigo-600', bg: 'bg-indigo-100' }
];

export default function LoadingResearch() {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev + 1) % steps.length);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex justify-start">
      <Card className="max-w-md p-6 bg-white border-2 border-gray-200 shadow-lg">
        <div className="space-y-4">
          <div className="flex items-center gap-3 mb-4">
            <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
            <span className="text-lg font-semibold text-gray-900">Researching...</span>
          </div>
          
          <div className="space-y-3">
            {steps.map((step, index) => {
              const Icon = step.icon;
              const isActive = index === currentStep;
              const isDone = index < currentStep;
              
              return (
                <div
                  key={index}
                  className={`flex items-center gap-3 p-3 rounded-lg transition-all duration-300 ${
                    isActive ? 'bg-blue-50 border-2 border-blue-300' : 'bg-gray-50 border-2 border-transparent'
                  }`}
                >
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                    isActive ? step.bg : 'bg-gray-200'
                  }`}>
                    <Icon className={`w-5 h-5 ${
                      isActive ? step.color : 'text-gray-400'
                    }`} />
                  </div>
                  <span className={`text-sm font-medium ${
                    isActive ? 'text-gray-900' : 'text-gray-500'
                  }`}>
                    {step.text}
                  </span>
                  {isDone && <CheckCircle2 className="w-4 h-4 text-green-600 ml-auto" />}
                  {isActive && <Loader2 className="w-4 h-4 animate-spin text-blue-600 ml-auto" />}
                </div>
              );
            })}
          </div>
        </div>
      </Card>
    </div>
  );
}