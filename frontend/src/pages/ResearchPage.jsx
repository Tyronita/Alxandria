import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, ArrowRight, ExternalLink, Loader2, CheckCircle2, Download, FileText, Package, Rocket } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const STEPS = [
  { num: 1, label: 'Papers & Analysis', icon: '📚' },
  { num: 2, label: 'Research Gaps', icon: '💡' },
  { num: 3, label: 'Select Dataset', icon: '📊' },
  { num: 4, label: 'Implementation', icon: '⚙️' },
  { num: 5, label: 'Ready to Ship', icon: '🚀' }
];

export default function ResearchPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const [stepData, setStepData] = useState({});
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [topic, setTopic] = useState('');
  const [sessionId] = useState(Date.now().toString());

  useEffect(() => {
    const initialQuery = location.state?.initialQuery;
    if (initialQuery) {
      setTopic(initialQuery);
      loadStep(1, initialQuery);
    }
  }, [location]);

  const loadStep = async (step, topicOverride = null) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/research/step`, {
        session_id: sessionId,
        topic: topicOverride || topic,
        step: step,
        selected_data: (step === 4 || step === 5) && selectedDataset ? { dataset_name: selectedDataset } : null
      });

      setStepData(prev => ({
        ...prev,
        [step]: {
          content: response.data.content,
          citations: response.data.citations || [],
          options: response.data.options
        }
      }));
      
      setCurrentStep(step);
      toast.success(`Step ${step} complete!`);
    } catch (error) {
      console.error('Step error:', error);
      toast.error('Failed to load step. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleNext = () => {
    if (currentStep === 3 && !selectedDataset) {
      toast.error('Please select a dataset first');
      return;
    }
    if (currentStep < 5) {
      loadStep(currentStep + 1);
    }
  };

  const handleDatasetSelect = (datasetName) => {
    setSelectedDataset(datasetName);
    toast.success(`Selected: ${datasetName}`);
  };

  const handleDownloadNotebook = async () => {
    try {
      const response = await axios.post(
        `${API}/ship/notebook`,
        {
          session_id: sessionId,
          topic: topic,
          dataset_name: selectedDataset || 'dataset'
        },
        { responseType: 'blob' }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `alexandria_${topic.replace(/\s+/g, '_')}.ipynb`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('Notebook downloaded!');
    } catch (error) {
      console.error('Download error:', error);
      toast.error('Failed to download notebook');
    }
  };

  const handleDownloadRequirements = async () => {
    try {
      const response = await axios.get(`${API}/ship/requirements`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'requirements.txt');
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('requirements.txt downloaded!');
    } catch (error) {
      console.error('Download error:', error);
      toast.error('Failed to download requirements');
    }
  };

  const currentData = stepData[currentStep];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <Button 
            variant="ghost" 
            size="sm"
            onClick={() => navigate('/')}
            data-testid="back-btn"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
          <img src="/alexandria-logo.png" alt="Alexandria" className="h-8" />
        </div>
      </header>

      {/* Progress Bar */}
      <div className="bg-white border-b">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {STEPS.map((step, idx) => (
              <React.Fragment key={step.num}>
                <div className="flex flex-col items-center">
                  <div
                    className={`w-12 h-12 rounded-full flex items-center justify-center text-xl transition-all ${
                      step.num < currentStep
                        ? 'bg-green-500 text-white'
                        : step.num === currentStep
                        ? 'bg-blue-500 text-white animate-pulse'
                        : 'bg-gray-200 text-gray-500'
                    }`}
                  >
                    {step.num < currentStep ? (
                      <CheckCircle2 className="w-6 h-6" />
                    ) : (
                      step.icon
                    )}
                  </div>
                  <span className="text-xs mt-2 font-medium text-gray-600">
                    {step.label}
                  </span>
                </div>
                {idx < STEPS.length - 1 && (
                  <div className={`flex-1 h-1 mx-2 ${
                    step.num < currentStep ? 'bg-green-500' : 'bg-gray-200'
                  }`} />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-5xl mx-auto px-6 py-8">
        {loading ? (
          <Card className="p-12 text-center">
            <Loader2 className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Loading Step {currentStep}...
            </h2>
            <p className="text-gray-600">{STEPS[currentStep - 1]?.label}</p>
          </Card>
        ) : currentData ? (
          <>
            <Card className="p-8 mb-6">
              <div className="flex items-center gap-2 mb-6">
                <span className="text-3xl">{STEPS[currentStep - 1]?.icon}</span>
                <h1 className="text-2xl font-bold text-gray-900">
                  {STEPS[currentStep - 1]?.label}
                </h1>
              </div>

              <div className="prose prose-lg max-w-none">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    table: ({node, ...props}) => (
                      <div className="overflow-x-auto my-4">
                        <table className="min-w-full border-collapse border border-gray-300" {...props} />
                      </div>
                    ),
                    th: ({node, ...props}) => (
                      <th className="border border-gray-300 bg-gray-100 px-4 py-2 text-left font-semibold" {...props} />
                    ),
                    td: ({node, ...props}) => (
                      <td className="border border-gray-300 px-4 py-2" {...props} />
                    ),
                    h2: ({node, ...props}) => (
                      <h2 className="text-2xl font-bold text-gray-900 mt-8 mb-4" {...props} />
                    ),
                    h3: ({node, ...props}) => (
                      <h3 className="text-xl font-bold text-gray-900 mt-6 mb-3" {...props} />
                    ),
                    code: ({node, inline, ...props}) => 
                      inline ? (
                        <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono" {...props} />
                      ) : (
                        <code className="block bg-gray-900 text-gray-100 p-4 rounded-lg text-sm font-mono overflow-x-auto" {...props} />
                      ),
                    a: ({node, ...props}) => (
                      <a className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer" {...props} />
                    )
                  }}
                >
                  {currentData.content}
                </ReactMarkdown>
              </div>

              {/* Dataset Selection */}
              {currentStep === 3 && (
                <div className="mt-8 pt-8 border-t">
                  <h3 className="text-lg font-semibold mb-4">Select Your Dataset:</h3>
                  <div className="grid gap-4">
                    {['Dataset Option 1', 'Dataset Option 2', 'Dataset Option 3'].map((name, idx) => (
                      <Card
                        key={idx}
                        onClick={() => handleDatasetSelect(name)}
                        className={`p-4 cursor-pointer transition-all ${
                          selectedDataset === name
                            ? 'border-2 border-blue-500 bg-blue-50'
                            : 'border hover:border-blue-300'
                        }`}
                        data-testid={`dataset-option-${idx}`}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <h4 className="font-semibold text-gray-900">{name}</h4>
                            <p className="text-sm text-gray-600">Click to select this dataset</p>
                          </div>
                          {selectedDataset === name && (
                            <CheckCircle2 className="w-6 h-6 text-blue-600" />
                          )}
                        </div>
                      </Card>
                    ))}
                  </div>
                </div>
              )}

              {/* Download Buttons on Step 5 */}
              {currentStep === 5 && (
                <div className="mt-8 pt-8 border-t">
                  <h3 className="text-lg font-semibold mb-4">🚀 Download Your Project</h3>
                  <div className="grid sm:grid-cols-2 gap-4">
                    <Button
                      onClick={handleDownloadNotebook}
                      className="h-20 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                      data-testid="download-notebook-btn"
                    >
                      <div className="flex flex-col items-center gap-2">
                        <Download className="w-6 h-6" />
                        <span>Download Notebook</span>
                      </div>
                    </Button>
                    
                    <Button
                      onClick={handleDownloadRequirements}
                      variant="outline"
                      className="h-20 border-2"
                      data-testid="download-requirements-btn"
                    >
                      <div className="flex flex-col items-center gap-2">
                        <FileText className="w-6 h-6" />
                        <span>Download requirements.txt</span>
                      </div>
                    </Button>
                  </div>
                </div>
              )}

              {/* Citations */}
              {currentData.citations?.length > 0 && (
                <div className="mt-8 pt-8 border-t">
                  <h3 className="text-lg font-semibold mb-3">Sources</h3>
                  <div className="flex flex-wrap gap-2">
                    {currentData.citations.map((citation, idx) => (
                      <a
                        key={idx}
                        href={citation.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 px-3 py-1 text-sm bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-full transition-colors"
                      >
                        {citation.title}
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </Card>

            {/* Navigation */}
            <div className="flex justify-between">
              <Button
                variant="outline"
                onClick={() => currentStep > 1 && setCurrentStep(currentStep - 1)}
                disabled={currentStep === 1}
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Previous
              </Button>
              
              {currentStep < 5 && (
                <Button
                  onClick={handleNext}
                  className="bg-blue-600 hover:bg-blue-700"
                  disabled={currentStep === 3 && !selectedDataset}
                  data-testid="next-step-btn"
                >
                  Next Step
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              )}
              
              {currentStep === 5 && (
                <Button
                  onClick={() => navigate('/ship', { 
                    state: { topic, dataset: selectedDataset, sessionId } 
                  })}
                  className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 px-8"
                  data-testid="ship-it-btn"
                >
                  <Rocket className="w-5 h-5 mr-2" />
                  Ship It!
                </Button>
              )}
            </div>
          </>
        ) : null}
      </div>
    </div>
  );
}