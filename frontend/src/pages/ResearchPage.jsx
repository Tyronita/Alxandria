import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { 
  ArrowLeft, 
  Sparkles,
  Send,
  Loader2,
  ExternalLink,
  Lightbulb,
  MessageSquare,
  ChevronRight,
  Check
} from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function ResearchPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const messagesEndRef = useRef(null);
  
  // Wizard state
  const [step, setStep] = useState('form'); // 'form', 'ideas', 'chat'
  
  // Form state
  const [interests, setInterests] = useState([]);
  const [frameworks, setFrameworks] = useState([]);
  const [cuttingEdge, setCuttingEdge] = useState([]);
  const [customInterest, setCustomInterest] = useState('');
  const [customFramework, setCustomFramework] = useState('');
  const [customCuttingEdge, setCustomCuttingEdge] = useState('');
  
  // Chat state
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  
  // Ideas state
  const [generatedIdeas, setGeneratedIdeas] = useState([]);
  const [selectedIdea, setSelectedIdea] = useState(null);

  const researchAreas = [
    'Natural Language Processing',
    'Medical Imaging & Disease Classification',
    'Fraud Detection & Security',
    'Computer Vision',
    'Reinforcement Learning',
    'Time Series Forecasting',
    'Generative AI',
    'Multimodal Learning'
  ];

  const frameworkOptions = [
    'PyTorch',
    'TensorFlow',
    'JAX',
    'Hugging Face Transformers',
    'LangChain',
    'FastAPI',
    'scikit-learn',
    'XGBoost'
  ];

  const cuttingEdgeTopics = [
    'Large Language Models (LLMs)',
    'Diffusion Models',
    'Retrieval Augmented Generation (RAG)',
    'Few-shot Learning',
    'Federated Learning',
    'Neural Architecture Search',
    'Explainable AI (XAI)',
    'Quantum Machine Learning'
  ];

  useEffect(() => {
    if (location.state?.selectedArea) {
      // Pre-select area from landing page
      const area = researchAreas.find(a => location.state.selectedArea.includes(a.split(' ')[0]));
      if (area) setInterests([area]);
    }
  }, [location]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleSelection = (item, list, setList) => {
    if (list.includes(item)) {
      setList(list.filter(i => i !== item));
    } else {
      setList([...list, item]);
    }
  };

  const addCustom = (value, list, setList, setClear) => {
    if (value.trim()) {
      setList([...list, value.trim()]);
      setClear('');
    }
  };

  const handleGenerateIdeas = async () => {
    if (interests.length === 0) {
      toast.error('Please select at least one area of interest');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/chat/generate-ideas`, {
        interests,
        frameworks,
        cutting_edge: cuttingEdge
      });
      
      setGeneratedIdeas(response.data.ideas || []);
      setStep('ideas');
      toast.success('Research ideas generated!');
    } catch (error) {
      console.error('Error generating ideas:', error);
      toast.error('Failed to generate ideas');
    } finally {
      setLoading(false);
    }
  };

  const startChat = (idea = null) => {
    const convId = Date.now().toString();
    setConversationId(convId);
    setSelectedIdea(idea);
    
    const initialMessage = {
      role: 'assistant',
      content: idea 
        ? `Great choice! Let's refine this idea: "${idea.title}". ${idea.description}\n\nWhat specific aspect interests you most? Or would you like to explore a different angle?`
        : `Hi! I'm your AI research assistant. Based on your interests in ${interests.join(', ')}, let's craft a cutting-edge research idea together. What problem or challenge would you like to tackle?`,
      timestamp: new Date().toISOString()
    };
    
    setMessages([initialMessage]);
    setStep('chat');
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
      const response = await axios.post(`${API}/chat/message`, {
        conversation_id: conversationId,
        message: currentMessage,
        context: {
          interests,
          frameworks,
          cutting_edge: cuttingEdge,
          selected_idea: selectedIdea
        },
        messages: messages
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        citations: response.data.citations || [],
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to send message');
      
      const errorMessage = {
        role: 'assistant',
        content: "I apologize, but I encountered an error. Please try again.",
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
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

  const CitationCard = ({ citation, index }) => (
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-xl sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              size="sm"
              onClick={() => step === 'form' ? navigate('/') : setStep('form')}
              data-testid="back-btn"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              {step === 'form' ? 'Home' : 'Back'}
            </Button>
            <div className="h-6 w-px bg-gray-300" />
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-600" />
              <span className="text-lg font-semibold text-gray-900">Research Assistant</span>
            </div>
          </div>
          
          {/* Progress indicator */}
          <div className="hidden sm:flex items-center gap-2 text-sm">
            <Badge variant={step === 'form' ? 'default' : 'secondary'}>1. Interests</Badge>
            <ChevronRight className="w-4 h-4 text-gray-400" />
            <Badge variant={step === 'ideas' ? 'default' : 'secondary'}>2. Ideas</Badge>
            <ChevronRight className="w-4 h-4 text-gray-400" />
            <Badge variant={step === 'chat' ? 'default' : 'secondary'}>3. Refine</Badge>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* STEP 1: Form */}
        {step === 'form' && (
          <div className="max-w-4xl mx-auto space-y-8">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-900 mb-3">
                Tell Us About Your Research Interests
              </h1>
              <p className="text-lg text-gray-600">
                Help us understand what you want to explore
              </p>
            </div>

            {/* Areas of Interest */}
            <Card className="p-6" data-testid="interests-card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-indigo-600" />
                Areas of Interest
              </h3>
              <div className="grid sm:grid-cols-2 gap-3 mb-4">
                {researchAreas.map((area) => (
                  <div
                    key={area}
                    onClick={() => toggleSelection(area, interests, setInterests)}
                    className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                      interests.includes(area)
                        ? 'border-indigo-500 bg-indigo-50'
                        : 'border-gray-200 hover:border-indigo-300'
                    }`}
                    data-testid={`interest-${area}`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                        interests.includes(area) ? 'bg-indigo-600 border-indigo-600' : 'border-gray-300'
                      }`}>
                        {interests.includes(area) && <Check className="w-3 h-3 text-white" />}
                      </div>
                      <span className="font-medium text-gray-900">{area}</span>
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex gap-2">
                <Input
                  placeholder="Add custom area..."
                  value={customInterest}
                  onChange={(e) => setCustomInterest(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addCustom(customInterest, interests, setInterests, setCustomInterest)}
                  data-testid="custom-interest-input"
                />
                <Button 
                  onClick={() => addCustom(customInterest, interests, setInterests, setCustomInterest)}
                  variant="outline"
                >
                  Add
                </Button>
              </div>
            </Card>

            {/* Frameworks */}
            <Card className="p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Frameworks & Technologies
              </h3>
              <div className="flex flex-wrap gap-2 mb-4">
                {frameworkOptions.map((framework) => (
                  <Badge
                    key={framework}
                    onClick={() => toggleSelection(framework, frameworks, setFrameworks)}
                    variant={frameworks.includes(framework) ? 'default' : 'outline'}
                    className="cursor-pointer text-sm py-2 px-4"
                    data-testid={`framework-${framework}`}
                  >
                    {framework}
                  </Badge>
                ))}
              </div>
              <div className="flex gap-2">
                <Input
                  placeholder="Add custom framework..."
                  value={customFramework}
                  onChange={(e) => setCustomFramework(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addCustom(customFramework, frameworks, setFrameworks, setCustomFramework)}
                />
                <Button 
                  onClick={() => addCustom(customFramework, frameworks, setFrameworks, setCustomFramework)}
                  variant="outline"
                >
                  Add
                </Button>
              </div>
            </Card>

            {/* Cutting Edge Topics */}
            <Card className="p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Cutting-Edge Topics You Want to Explore
              </h3>
              <div className="flex flex-wrap gap-2 mb-4">
                {cuttingEdgeTopics.map((topic) => (
                  <Badge
                    key={topic}
                    onClick={() => toggleSelection(topic, cuttingEdge, setCuttingEdge)}
                    variant={cuttingEdge.includes(topic) ? 'default' : 'outline'}
                    className="cursor-pointer text-sm py-2 px-4"
                    data-testid={`topic-${topic}`}
                  >
                    {topic}
                  </Badge>
                ))}
              </div>
              <div className="flex gap-2">
                <Input
                  placeholder="Add custom topic..."
                  value={customCuttingEdge}
                  onChange={(e) => setCustomCuttingEdge(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addCustom(customCuttingEdge, cuttingEdge, setCuttingEdge, setCustomCuttingEdge)}
                />
                <Button 
                  onClick={() => addCustom(customCuttingEdge, cuttingEdge, setCuttingEdge, setCustomCuttingEdge)}
                  variant="outline"
                >
                  Add
                </Button>
              </div>
            </Card>

            <div className="flex justify-center pt-4">
              <Button
                onClick={handleGenerateIdeas}
                disabled={loading || interests.length === 0}
                size="lg"
                className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-lg px-8 py-6"
                data-testid="generate-ideas-btn"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Generating Ideas...
                  </>
                ) : (
                  <>
                    Generate Research Ideas
                    <Sparkles className="w-5 h-5 ml-2" />
                  </>
                )}
              </Button>
            </div>
          </div>
        )}

        {/* STEP 2: Generated Ideas */}
        {step === 'ideas' && (
          <div className="max-w-5xl mx-auto space-y-6">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-900 mb-3">
                Curated Research Ideas
              </h1>
              <p className="text-lg text-gray-600">
                Pick an idea to refine, or start from scratch
              </p>
            </div>

            <div className="grid gap-6">
              {generatedIdeas.map((idea, index) => (
                <Card 
                  key={index}
                  className="p-6 hover:shadow-xl transition-all cursor-pointer border-2 hover:border-indigo-400"
                  onClick={() => startChat(idea)}
                  data-testid={`idea-card-${index}`}
                >
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-gray-900 mb-2">{idea.title}</h3>
                      <p className="text-gray-600 mb-3">{idea.description}</p>
                      <div className="flex flex-wrap gap-2">
                        {idea.tags?.map((tag, idx) => (
                          <Badge key={idx} variant="secondary">{tag}</Badge>
                        ))}
                      </div>
                    </div>
                    <ChevronRight className="w-6 h-6 text-gray-400" />
                  </div>
                </Card>
              ))}

              <Card 
                className="p-6 border-2 border-dashed border-gray-300 hover:border-indigo-400 hover:bg-indigo-50 transition-all cursor-pointer"
                onClick={() => startChat()}
                data-testid="start-from-scratch"
              >
                <div className="text-center py-4">
                  <MessageSquare className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-lg font-semibold text-gray-900 mb-1">Start From Scratch</p>
                  <p className="text-gray-600">Create your own research idea with AI guidance</p>
                </div>
              </Card>
            </div>
          </div>
        )}

        {/* STEP 3: Multi-turn Chat */}
        {step === 'chat' && (
          <div className="max-w-5xl mx-auto">
            <Card className="h-[calc(100vh-200px)] flex flex-col">
              {/* Chat messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4" data-testid="chat-messages">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                        message.role === 'user'
                          ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <div className="whitespace-pre-wrap">{message.content}</div>
                      {message.citations && message.citations.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-3 pt-3 border-t border-gray-300">
                          {message.citations.map((citation, idx) => (
                            <CitationCard key={idx} citation={citation} index={idx} />
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 rounded-2xl px-4 py-3">
                      <Loader2 className="w-5 h-5 animate-spin text-gray-600" />
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input area */}
              <div className="border-t p-4">
                <div className="flex gap-2">
                  <Textarea
                    placeholder="Type your message... (Shift+Enter for new line)"
                    value={currentMessage}
                    onChange={(e) => setCurrentMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    className="resize-none"
                    rows={2}
                    data-testid="chat-input"
                  />
                  <Button
                    onClick={sendMessage}
                    disabled={loading || !currentMessage.trim()}
                    className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700"
                    data-testid="send-btn"
                  >
                    <Send className="w-5 h-5" />
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}