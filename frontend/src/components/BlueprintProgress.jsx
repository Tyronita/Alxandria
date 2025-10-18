import React from 'react';
import { Card } from '@/components/ui/card';
import { Check, Circle, ArrowRight } from 'lucide-react';

const stages = [
  { key: 'curiosity', label: 'Curiosity', icon: '💭' },
  { key: 'papers', label: 'Papers', icon: '📚' },
  { key: 'gaps', label: 'Research Gaps', icon: '💡' },
  { key: 'dataset', label: 'Dataset', icon: '📊' },
  { key: 'implementation', label: 'Implementation', icon: '⚙️' }
];

export default function BlueprintProgress({ currentStage, completedStages = [] }) {
  return (
    <Card className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Research Blueprint Progress</h3>
      <div className="flex items-center justify-between">
        {stages.map((stage, index) => {
          const isCompleted = completedStages.includes(stage.key);
          const isCurrent = currentStage === stage.key;
          
          return (
            <React.Fragment key={stage.key}>
              <div className="flex flex-col items-center">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center text-xl transition-all ${
                    isCompleted
                      ? 'bg-green-500 shadow-lg'
                      : isCurrent
                      ? 'bg-blue-500 shadow-lg animate-pulse'
                      : 'bg-gray-300'
                  }`}
                >
                  {isCompleted ? (
                    <Check className="w-6 h-6 text-white" />
                  ) : (
                    <span>{stage.icon}</span>
                  )}
                </div>
                <span
                  className={`text-xs mt-2 font-medium ${
                    isCurrent ? 'text-blue-700' : 'text-gray-600'
                  }`}
                >
                  {stage.label}
                </span>
              </div>
              {index < stages.length - 1 && (
                <ArrowRight
                  className={`w-4 h-4 ${
                    isCompleted ? 'text-green-500' : 'text-gray-300'
                  }`}
                />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </Card>
  );
}
