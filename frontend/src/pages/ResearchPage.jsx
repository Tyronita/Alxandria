import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  ArrowLeft, 
  Sparkles,
  Send,
  Loader2,
  ExternalLink,
  BookOpen,
  Lightbulb,
  TrendingUp,
  Rocket
} from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function ResearchPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const messagesEndRef = useRef(null);
  
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(Date.now().toString());

  useEffect(() => {
    const initialQuery = location.state?.initialQuery;
    if (initialQuery) {
      // Start conversation with user's initial query
      startConversation(initialQuery);
    } else {
      // Start with welcome message
      const welcomeMessage = {
        role: 'assistant',
        content: "Hi! I'm your AI research guide. What would you like to learn about today? Share your curiosity, and I'll help you explore cutting-edge research, discover novel ideas, and guide you toward an actionable research direction.",
        timestamp: new Date().toISOString()
      };
      setMessages([welcomeMessage]);
    }
  }, [location]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const startConversation = async (query) => {
    const userMessage = {
      role: 'user',
      content: query,
      timestamp: new Date().toISOString()
    };
    setMessages([userMessage]);
    setLoading(true);

    try {
      const response = await axios.post(`${API}/chat/converse`, {
        session_id: sessionId,
        message: query,
        is_initial: true
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        citations: response.data.citations || [],
        research_cards: response.data.research_cards || [],
        timestamp: new Date().toISOString()
      };

      setMessages([userMessage, assistantMessage]);
    } catch (error) {
      console.error('Error starting conversation:', error);
      toast.error('Failed to start conversation');
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!currentMessage.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: currentMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setLoading(true);

    try {
      const response = await axios.post(`${API}/chat/converse`, {
        session_id: sessionId,
        message: currentMessage,
        conversation_history: messages.slice(-6)
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        citations: response.data.citations || [],
        research_cards: response.data.research_cards || [],
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const CitationBadge = ({ citation, index }) => (
    <a
      href={citation.url}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-1 px-2 py-1 text-xs bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-md transition-colors"
      data-testid={`citation-${index}`}
    >
      <span className="font-medium text-blue-700">[{index + 1}]</span>
      <ExternalLink className="w-3 h-3 text-blue-600" />
    </a>
  );

  const ResearchCard = ({ card, index }) => (
    <Card className="p-4 bg-gradient-to-br from-white to-blue-50 border-2 border-blue-100">
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center text-white">
          {card.type === 'research' ? <BookOpen className="w-5 h-5" /> : 
           card.type === 'idea' ? <Lightbulb className="w-5 h-5" /> : 
           <TrendingUp className="w-5 h-5" />}
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-gray-900 mb-1">{card.title}</h4>
          <p className="text-sm text-gray-600">{card.description}</p>
        </div>
      </div>
    </Card>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-xl sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              size="sm"
              onClick={() => navigate('/')}
              data-testid="back-home-btn"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Home
            </Button>
            <Separator orientation="vertical" className="h-6" />
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-blue-600" />
              <span className="text-lg font-semibold text-gray-900">Research Journey</span>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Interface */}
      <div className="max-w-5xl mx-auto px-6 py-8">
        <Card className="h-[calc(100vh-180px)] flex flex-col shadow-xl border-2 border-gray-200">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6" data-testid="chat-messages">
            {messages.map((message, index) => (
              <div key={index}>
                <div
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] rounded-2xl px-5 py-4 ${
                      message.role === 'user'
                        ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg'
                        : 'bg-white border-2 border-gray-200 text-gray-900 shadow-md'
                    }`}
                  >
                    <div className="whitespace-pre-wrap leading-relaxed">{message.content}</div>
                    
                    {/* Citations */}
                    {message.citations && message.citations.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-gray-200">
                        <span className="text-xs text-gray-500 font-medium">Sources:</span>
                        {message.citations.map((citation, idx) => (
                          <CitationBadge key={idx} citation={citation} index={idx} />
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* Research Cards */}
                {message.research_cards && message.research_cards.length > 0 && (
                  <div className="mt-4 space-y-3 ml-12">
                    {message.research_cards.map((card, cardIdx) => (
                      <ResearchCard key={cardIdx} card={card} index={cardIdx} />
                    ))}
                  </div>
                )}
              </div>
            ))}
            
            {loading && (
              <div className="flex justify-start">
                <div className="bg-white border-2 border-gray-200 rounded-2xl px-5 py-4 shadow-md">
                  <div className="flex items-center gap-2">
                    <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
                    <span className="text-gray-600">Researching...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t-2 border-gray-200 p-4 bg-gray-50">
            <div className="flex gap-3">
              <Input
                placeholder="Ask a question, share thoughts, or request clarification..."
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                className="flex-1 h-12 border-2 border-gray-300 focus:border-blue-500"
                data-testid="message-input"
              />
              <Button
                onClick={sendMessage}
                disabled={loading || !currentMessage.trim()}
                size="lg"
                className="h-12 px-6 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                data-testid="send-btn"
              >
                <Send className="w-5 h-5" />
              </Button>
            </div>
            <p className="text-xs text-gray-500 mt-2 text-center">
              Press Enter to send • Shift+Enter for new line
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
}