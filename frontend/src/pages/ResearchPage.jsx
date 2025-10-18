import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, ExternalLink, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function ResearchPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(false);
  const [blueprint, setBlueprint] = useState(null);
  const [citations, setCitations] = useState([]);
  const [sessionId] = useState(Date.now().toString());

  useEffect(() => {
    const initialQuery = location.state?.initialQuery;
    if (initialQuery) {
      startResearch(initialQuery);
    }
  }, [location]);

  const startResearch = async (query) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/research/complete`, {
        session_id: sessionId,
        message: query,
        conversation_history: []
      });

      setBlueprint(response.data.response);
      setCitations(response.data.citations || []);
      toast.success('Research complete!');
    } catch (error) {
      console.error('Research error:', error);
      toast.error('Research failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

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

      {/* Content */}
      <div className="max-w-5xl mx-auto px-6 py-8">
        {loading && (
          <Card className="p-12 text-center">
            <Loader2 className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Researching...</h2>
            <p className="text-gray-600">Finding papers, datasets, and creating your research blueprint</p>
          </Card>
        )}

        {blueprint && (
          <Card className="p-8">
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
                  strong: ({node, ...props}) => (
                    <strong className="font-bold text-gray-900" {...props} />
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
                {blueprint}
              </ReactMarkdown>
            </div>

            {citations.length > 0 && (
              <div className="mt-8 pt-8 border-t">
                <h3 className="text-lg font-semibold mb-3">Sources</h3>
                <div className="flex flex-wrap gap-2">
                  {citations.map((citation, idx) => (
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
        )}
      </div>
    </div>
  );
}