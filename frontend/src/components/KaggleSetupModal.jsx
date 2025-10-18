import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { X, ExternalLink, AlertCircle, CheckCircle2 } from 'lucide-react';
import { toast } from 'sonner';

export default function KaggleSetupModal({ isOpen, onClose, onSave }) {
  const [username, setUsername] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [showInstructions, setShowInstructions] = useState(false);

  const handleSave = () => {
    if (!username.trim() || !apiKey.trim()) {
      toast.error('Please enter both username and API key');
      return;
    }

    // Validate format
    if (apiKey.length < 20) {
      toast.error('API key seems too short. Please check and try again.');
      return;
    }

    // Save to localStorage
    const credentials = {
      username: username.trim(),
      key: apiKey.trim()
    };
    
    localStorage.setItem('kaggle_credentials', JSON.stringify(credentials));
    toast.success('Kaggle credentials saved!');
    onSave(credentials);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <Card className="max-w-2xl w-full max-h-[90vh] overflow-y-auto bg-white">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Setup Kaggle API</h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Phone Verification Warning */}
          <div className="bg-orange-50 border-2 border-orange-300 rounded-lg p-4 mb-6">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-6 h-6 text-orange-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-orange-900 mb-1">
                  Phone Verification Required
                </h3>
                <p className="text-sm text-orange-800 mb-2">
                  Before using the Kaggle API to publish notebooks, you MUST verify your phone number on Kaggle.
                </p>
                <a
                  href="https://www.kaggle.com/settings"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-sm font-medium text-orange-700 hover:text-orange-900 hover:underline"
                >
                  Verify Phone Number on Kaggle
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>
            </div>
          </div>

          {/* Instructions Toggle */}
          <Button
            variant="outline"
            onClick={() => setShowInstructions(!showInstructions)}
            className="mb-4 w-full"
          >
            {showInstructions ? '▼' : '▶'} How to get your Kaggle API credentials
          </Button>

          {/* Instructions */}
          {showInstructions && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 space-y-3">
              <h3 className="font-semibold text-blue-900 mb-2">Step-by-Step Instructions:</h3>
              
              <div className="space-y-2 text-sm text-blue-800">
                <div className="flex items-start gap-2">
                  <span className="font-semibold">1.</span>
                  <div>
                    Go to{' '}
                    <a
                      href="https://www.kaggle.com/settings/account"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline inline-flex items-center gap-1"
                    >
                      Kaggle Account Settings
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
                
                <div className="flex items-start gap-2">
                  <span className="font-semibold">2.</span>
                  <span>Scroll down to the "API" section</span>
                </div>
                
                <div className="flex items-start gap-2">
                  <span className="font-semibold">3.</span>
                  <span>Click "Create New Token" button</span>
                </div>
                
                <div className="flex items-start gap-2">
                  <span className="font-semibold">4.</span>
                  <span>A file named <code className="bg-blue-100 px-1 rounded">kaggle.json</code> will download</span>
                </div>
                
                <div className="flex items-start gap-2">
                  <span className="font-semibold">5.</span>
                  <span>Open the file - it contains your username and key in this format:</span>
                </div>
              </div>

              <div className="bg-gray-800 text-gray-100 p-3 rounded font-mono text-xs overflow-x-auto">
                {'{"username":"your_username","key":"abc123...xyz"}'}
              </div>

              <div className="text-sm text-blue-800 mt-2">
                <strong>Important:</strong> Keep your API key secret! Don't share it publicly.
              </div>
            </div>
          )}

          {/* Input Form */}
          <div className="space-y-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Kaggle Username
              </label>
              <Input
                type="text"
                placeholder="your_kaggle_username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Kaggle API Key
              </label>
              <Input
                type="password"
                placeholder="Your API key from kaggle.json"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="w-full font-mono text-sm"
              />
              <p className="text-xs text-gray-500 mt-1">
                This will be stored locally in your browser only
              </p>
            </div>
          </div>

          {/* Verification Checklist */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-green-900 mb-3 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5" />
              Pre-flight Checklist
            </h3>
            <div className="space-y-2 text-sm text-green-800">
              <div className="flex items-center gap-2">
                <input type="checkbox" id="check1" className="rounded" />
                <label htmlFor="check1">Phone number verified on Kaggle</label>
              </div>
              <div className="flex items-center gap-2">
                <input type="checkbox" id="check2" className="rounded" />
                <label htmlFor="check2">Downloaded kaggle.json from settings</label>
              </div>
              <div className="flex items-center gap-2">
                <input type="checkbox" id="check3" className="rounded" />
                <label htmlFor="check3">Entered username and key above</label>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <Button
              onClick={handleSave}
              className="flex-1 bg-blue-600 hover:bg-blue-700 h-12 text-lg"
            >
              Save Credentials
            </Button>
            <Button
              onClick={onClose}
              variant="outline"
              className="px-6 h-12"
            >
              Cancel
            </Button>
          </div>

          {/* Privacy Note */}
          <p className="text-xs text-gray-500 text-center mt-4">
            Your credentials are stored locally in your browser and never sent to our servers.
            They are only used to push notebooks directly to your Kaggle account.
          </p>
        </div>
      </Card>
    </div>
  );
}
