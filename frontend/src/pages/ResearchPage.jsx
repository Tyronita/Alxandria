import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import { 
  ArrowLeft, 
  Search, 
  BookOpen, 
  Target, 
  Lightbulb, 
  Sparkles,
  ExternalLink,
  Loader2,
  AlertCircle,
  CheckCircle2
} from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function ResearchPage() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [activeTab, setActiveTab] = useState('refine');
  const [loading, setLoading] = useState(false);
  
  // Results state
  const [refineResult, setRefineResult] = useState(null);
  const [taskSpec, setTaskSpec] = useState(null);
  const [sotaReview, setSotaReview] = useState(null);
  const [techniques, setTechniques] = useState(null);
  const [recommendation, setRecommendation] = useState(null);

  const handleRefineResearch = async () => {
    if (!query.trim()) {
      toast.error('Please enter a research query');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/research/refine`, {
        query: query,
        domain_filter: ['arxiv.org', 'github.com', 'kaggle.com', 'huggingface.co']
      });
      
      setRefineResult(response.data);
      toast.success('Research refined successfully!');
      setActiveTab('results');
    } catch (error) {
      console.error('Error refining research:', error);
      toast.error('Failed to refine research. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateTaskSpec = async () => {
    if (!refineResult?.query_id) {
      toast.error('Please refine your research first');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/research/task-spec`, {
        query_id: refineResult.query_id
      });
      
      setTaskSpec(response.data);
      toast.success('Task specification generated!');
    } catch (error) {
      console.error('Error generating task spec:', error);
      toast.error('Failed to generate task specification.');
    } finally {
      setLoading(false);
    }
  };

  const handleGetSOTAReview = async () => {
    if (!query.trim()) {
      toast.error('Please enter a research topic');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/research/sota-review`, {
        topic: query,
        domain_filter: ['arxiv.org', 'nature.com', 'science.org']
      });
      
      setSotaReview(response.data);
      toast.success('SOTA review generated!');
    } catch (error) {
      console.error('Error getting SOTA review:', error);
      toast.error('Failed to generate SOTA review.');
    } finally {
      setLoading(false);
    }
  };

  const handleFindTechniques = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/research/techniques`, {
        dataset_type: 'tabular',
        problem_type: 'classification'
      });
      
      setTechniques(response.data);
      toast.success('Techniques found!');
    } catch (error) {
      console.error('Error finding techniques:', error);
      toast.error('Failed to find techniques.');
    } finally {
      setLoading(false);
    }
  };

  const handleGetRecommendation = async () => {
    if (!refineResult?.query_id) {
      toast.error('Please refine your research first');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/research/recommend`, {
        query_id: refineResult.query_id,
        context: 'Machine learning project'
      });
      
      setRecommendation(response.data);
      toast.success('Recommendation generated!');
    } catch (error) {
      console.error('Error getting recommendation:', error);
      toast.error('Failed to generate recommendation.');
    } finally {
      setLoading(false);
    }
  };

  const CitationCard = ({ citation, index }) => (
    <a
      href={citation.url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-start gap-3 p-3 rounded-lg border border-gray-200 hover:border-blue-400 hover:bg-blue-50 transition-all group"
      data-testid={`citation-${index}`}
    >
      <Badge variant="secondary" className="mt-1">{index + 1}</Badge>
      <div className="flex-1 min-w-0">
        <p className="font-medium text-gray-900 group-hover:text-blue-600 line-clamp-1">
          {citation.title}
        </p>
        <p className="text-sm text-gray-500 line-clamp-1">{citation.url}</p>
        {citation.date && (
          <p className="text-xs text-gray-400 mt-1">{citation.date}</p>
        )}
      </div>
      <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-blue-600" />
    </a>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 via-white to-blue-50">
      {/* Header */}
      <header className="border-b bg-white/70 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              size="sm"
              onClick={() => navigate('/')}
              data-testid="back-to-home-btn"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <Separator orientation="vertical" className="h-6" />
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-blue-600" />
              <span className="text-lg font-semibold text-gray-900">Research Assistant</span>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Query Input */}
        <Card className="p-6 mb-8 bg-white shadow-sm" data-testid="query-input-card">
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-700 mb-2 block">
                Research Query
              </label>
              <Textarea
                placeholder="Enter your research question or topic (e.g., 'best practices for tabular classification on Kaggle Titanic dataset')..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="min-h-[100px] text-base"
                data-testid="research-query-input"
              />
            </div>
            
            <div className="flex gap-3">
              <Button
                onClick={handleRefineResearch}
                disabled={loading || !query.trim()}
                className="bg-blue-600 hover:bg-blue-700"
                data-testid="refine-research-btn"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Search className="w-4 h-4 mr-2" />
                    Refine Research
                  </>
                )}
              </Button>
              
              {refineResult && (
                <>
                  <Button
                    variant="outline"
                    onClick={handleGenerateTaskSpec}
                    disabled={loading}
                    data-testid="gen-task-spec-btn"
                  >
                    <Target className="w-4 h-4 mr-2" />
                    Generate Task Spec
                  </Button>
                  
                  <Button
                    variant="outline"
                    onClick={handleGetSOTAReview}
                    disabled={loading}
                    data-testid="sota-review-btn"
                  >
                    <BookOpen className="w-4 h-4 mr-2" />
                    SOTA Review
                  </Button>
                  
                  <Button
                    variant="outline"
                    onClick={handleGetRecommendation}
                    disabled={loading}
                    data-testid="get-recommendation-btn"
                  >
                    <Lightbulb className="w-4 h-4 mr-2" />
                    Get Recommendation
                  </Button>
                </>
              )}
            </div>
          </div>
        </Card>

        {/* Results Section */}
        {refineResult && (
          <div className="space-y-6">
            {/* Refined Research */}
            <Card className="p-6 bg-white shadow-sm" data-testid="refined-research-card">
              <div className="flex items-center gap-2 mb-4">
                <CheckCircle2 className="w-5 h-5 text-green-600" />
                <h2 className="text-2xl font-bold text-gray-900">Refined Research</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Problem Statement</h3>
                  <p className="text-gray-800">{refineResult.problem_statement}</p>
                </div>
                
                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">AI Analysis</h3>
                  <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                    {refineResult.raw_content}
                  </div>
                </div>

                {refineResult.citations && refineResult.citations.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-gray-500 uppercase mb-3">Sources & Citations</h3>
                    <div className="space-y-2">
                      {refineResult.citations.map((citation, idx) => (
                        <CitationCard key={idx} citation={citation} index={idx} />
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </Card>

            {/* Task Specification */}
            {taskSpec && (
              <Card className="p-6 bg-white shadow-sm" data-testid="task-spec-card">
                <div className="flex items-center gap-2 mb-4">
                  <Target className="w-5 h-5 text-blue-600" />
                  <h2 className="text-2xl font-bold text-gray-900">Task Specification</h2>
                </div>
                
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Task Name</h3>
                    <p className="text-gray-800">{taskSpec.task_name}</p>
                  </div>
                  
                  <div>
                    <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Target Metric</h3>
                    <Badge variant="outline" className="text-sm">{taskSpec.target_metric}</Badge>
                  </div>
                  
                  <div className="md:col-span-2">
                    <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Dataset Candidates</h3>
                    <div className="flex flex-wrap gap-2">
                      {taskSpec.dataset_candidates.map((dataset, idx) => (
                        <Badge key={idx} variant="secondary">{dataset}</Badge>
                      ))}
                    </div>
                  </div>
                  
                  <div className="md:col-span-2">
                    <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Deliverables</h3>
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                      {taskSpec.deliverables.map((item, idx) => (
                        <li key={idx}>{item}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </Card>
            )}

            {/* SOTA Review */}
            {sotaReview && (
              <Card className="p-6 bg-white shadow-sm" data-testid="sota-review-card">
                <div className="flex items-center gap-2 mb-4">
                  <BookOpen className="w-5 h-5 text-purple-600" />
                  <h2 className="text-2xl font-bold text-gray-900">State-of-the-Art Review</h2>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Summary</h3>
                    <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                      {sotaReview.summary}
                    </div>
                  </div>
                  
                  {sotaReview.citations && sotaReview.citations.length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-500 uppercase mb-3">Research Sources</h3>
                      <div className="space-y-2">
                        {sotaReview.citations.map((citation, idx) => (
                          <CitationCard key={idx} citation={citation} index={idx} />
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </Card>
            )}

            {/* Recommendation */}
            {recommendation && (
              <Card className="p-6 bg-gradient-to-br from-amber-50 to-orange-50 border-amber-200 shadow-sm" data-testid="recommendation-card">
                <div className="flex items-center gap-2 mb-4">
                  <Lightbulb className="w-5 h-5 text-amber-600" />
                  <h2 className="text-2xl font-bold text-gray-900">Recommended Technique</h2>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <Badge className="bg-amber-500 hover:bg-amber-600 mb-3">
                      {recommendation.technique_name}
                    </Badge>
                    <p className="text-gray-800">{recommendation.why_it_fits}</p>
                  </div>
                  
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="bg-white p-4 rounded-lg border border-amber-200">
                      <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Expected Gain</h3>
                      <p className="text-green-700 font-medium">{recommendation.expected_metric_gain}</p>
                    </div>
                    
                    <div className="bg-white p-4 rounded-lg border border-amber-200">
                      <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Risks</h3>
                      <ul className="text-gray-700 space-y-1">
                        {recommendation.risks.map((risk, idx) => (
                          <li key={idx} className="flex items-start gap-2">
                            <AlertCircle className="w-4 h-4 text-amber-600 mt-0.5" />
                            <span className="text-sm">{risk}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                  
                  {recommendation.evidence && recommendation.evidence.length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-500 uppercase mb-3">Supporting Evidence</h3>
                      <div className="space-y-2">
                        {recommendation.evidence.map((citation, idx) => (
                          <CitationCard key={idx} citation={citation} index={idx} />
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </Card>
            )}
          </div>
        )}

        {/* Empty State */}
        {!refineResult && (
          <Card className="p-12 text-center bg-white/50 border-dashed" data-testid="empty-state">
            <Search className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">
              Start Your Research Journey
            </h3>
            <p className="text-gray-500">
              Enter a research query above and click "Refine Research" to begin
            </p>
          </Card>
        )}
      </div>
    </div>
  );
}