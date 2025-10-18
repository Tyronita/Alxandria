import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Database, Wrench, FileCheck, Rocket, ExternalLink } from 'lucide-react';

export default function ResearchChecklist({ onComplete }) {
  const [checklist, setChecklist] = React.useState({
    dataset: false,
    method: false,
    justification: false
  });

  const items = [
    {
      key: 'dataset',
      icon: Database,
      title: 'Dataset Selected',
      description: 'Choose your target dataset from the research above'
    },
    {
      key: 'method',
      icon: Wrench,
      title: 'Method/Technique Picked',
      description: 'Select the approach you want to implement'
    },
    {
      key: 'justification',
      icon: FileCheck,
      title: 'Understand Justification',
      description: 'Review why this method works for your problem'
    }
  ];

  const toggleItem = (key) => {
    setChecklist(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const allChecked = Object.values(checklist).every(v => v);

  return (
    <Card className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 mt-4">
      <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
        <Rocket className="w-5 h-5 text-blue-600" />
        Ready to Build?
      </h3>
      
      <div className="space-y-3 mb-6">
        {items.map((item) => {
          const Icon = item.icon;
          const checked = checklist[item.key];
          
          return (
            <div
              key={item.key}
              onClick={() => toggleItem(item.key)}
              className={`flex items-start gap-3 p-4 rounded-lg border-2 cursor-pointer transition-all ${
                checked
                  ? 'bg-white border-green-400 shadow-md'
                  : 'bg-white/50 border-gray-300 hover:border-blue-400'
              }`}
            >
              <Checkbox
                checked={checked}
                className="mt-1"
                data-testid={`checklist-${item.key}`}
              />
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <Icon className={`w-5 h-5 ${
                    checked ? 'text-green-600' : 'text-gray-400'
                  }`} />
                  <h4 className="font-semibold text-gray-900">{item.title}</h4>
                </div>
                <p className="text-sm text-gray-600">{item.description}</p>
              </div>
            </div>
          );
        })}
      </div>

      <Button
        onClick={onComplete}
        disabled={!allChecked}
        className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50"
        data-testid="ready-to-build-btn"
      >
        <Rocket className="w-5 h-5 mr-2" />
        {allChecked ? "Let's Build This!" : 'Complete Checklist First'}
      </Button>
      
      {allChecked && (
        <p className="text-center text-sm text-green-700 mt-3 font-medium">
          Great! You're ready to start implementing.
        </p>
      )}
    </Card>
  );
}