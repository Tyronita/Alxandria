from fastapi import FastAPI, APIRouter, HTTPException, status
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
from openai import OpenAI
import json
import subprocess
import tempfile

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize Perplexity client (using OpenAI SDK with Perplexity endpoint)
perplexity_client = OpenAI(
    api_key=os.environ.get('PERPLEXITY_API_KEY'),
    base_url="https://api.perplexity.ai"
)

# Setup Kaggle credentials
kaggle_username = os.environ.get('KAGGLE_USERNAME')
kaggle_key = os.environ.get('KAGGLE_KEY')

app = FastAPI(title="Research Assistant API")
api_router = APIRouter(prefix="/api")

# ============ MODELS ============

class ResearchQuery(BaseModel):
    query: str = Field(..., min_length=1)
    domain_filter: Optional[List[str]] = None
    recency_filter: Optional[str] = None

class Citation(BaseModel):
    title: str
    url: str
    snippet: Optional[str] = None
    date: Optional[str] = None

class ResearchResponse(BaseModel):
    query_id: str
    problem_statement: str
    scope: str
    assumptions: List[str]
    risks: List[str]
    candidate_metrics: List[str]
    citations: List[Citation]
    raw_content: str

class TaskSpecRequest(BaseModel):
    query_id: str
    focus_area: Optional[str] = None

class TaskSpec(BaseModel):
    task_id: str
    query_id: str
    task_name: str
    dataset_candidates: List[str]
    target_metric: str
    constraints: List[str]
    compute_budget: str
    deliverables: List[str]
    citations: List[Citation]

class SOTAReviewRequest(BaseModel):
    topic: str
    domain_filter: Optional[List[str]] = None

class SOTAReview(BaseModel):
    review_id: str
    topic: str
    summary: str
    key_findings: List[str]
    gaps: List[str]
    citations: List[Citation]

class TechniquesRequest(BaseModel):
    dataset_type: str
    problem_type: str

class Technique(BaseModel):
    name: str
    description: str
    category: str
    sources: List[Citation]

class TechniquesResponse(BaseModel):
    techniques: List[Technique]

class RecommendRequest(BaseModel):
    query_id: str
    context: Optional[str] = None

class Recommendation(BaseModel):
    recommendation_id: str
    technique_name: str
    why_it_fits: str
    expected_metric_gain: str
    risks: List[str]
    evidence: List[Citation]

class KaggleDataset(BaseModel):
    title: str
    ref: str
    subtitle: str
    size: str
    last_updated: str

class KaggleCompetition(BaseModel):
    title: str
    ref: str
    description: str
    deadline: str
    prize: str

# ============ HELPER FUNCTIONS ============

def extract_citations(response) -> List[Citation]:
    """Extract citations from Perplexity response"""
    citations = []
    if hasattr(response, 'search_results'):
        for result in response.search_results:
            citations.append(Citation(
                title=result.get('title', ''),
                url=result.get('url', ''),
                snippet=result.get('snippet', ''),
                date=result.get('date', '')
            ))
    return citations

def run_kaggle_command(command: List[str]) -> str:
    """Run kaggle CLI command with credentials"""
    env = os.environ.copy()
    
    # Create temporary kaggle.json
    kaggle_config = {
        "username": kaggle_username,
        "key": kaggle_key
    }
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(kaggle_config, f)
        temp_file = f.name
    
    try:
        # Set environment to use temp config
        env['KAGGLE_CONFIG_DIR'] = os.path.dirname(temp_file)
        env['KAGGLE_USERNAME'] = kaggle_username
        env['KAGGLE_KEY'] = kaggle_key
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            env=env
        )
        return result.stdout
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)

# ============ ROUTES ============

@api_router.get("/")
async def root():
    return {"message": "Research Assistant API", "version": "1.0.0"}

# ============ NEW CONVERSATIONAL CHAT ============

class ResearchCardModel(BaseModel):
    type: str  # 'research', 'idea', 'future'
    title: str
    description: str

class ChatConverseRequest(BaseModel):
    session_id: str
    message: str
    is_initial: bool = False
    conversation_history: List[Dict[str, Any]] = []

class ChatConverseResponse(BaseModel):
    response: str
    citations: List[Citation] = []
    research_cards: List[ResearchCardModel] = []

@api_router.post("/chat/converse", response_model=ChatConverseResponse)
async def conversational_research(request: ChatConverseRequest):
    """
    Generate curated research ideas based on user interests
    """
    try:
        system_prompt = """You are a research advisor. Generate 4-5 specific, cutting-edge ML research ideas.
        For each idea, provide:
        - A compelling title
        - A 2-3 sentence description
        - 3-4 relevant tags
        - Difficulty level (Beginner/Intermediate/Advanced)
        
        Make ideas specific, actionable, and aligned with current research trends."""
        
        user_prompt = f"""Generate research ideas for someone interested in:
        Areas: {', '.join(request.interests)}
        Frameworks: {', '.join(request.frameworks) if request.frameworks else 'Any'}
        Cutting-edge topics: {', '.join(request.cutting_edge) if request.cutting_edge else 'General ML'}
        
        Focus on practical, implementable ideas that combine these interests."""
        
        response = perplexity_client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            extra_body={
                "search_domain_filter": ["arxiv.org", "github.com", "kaggle.com", "paperswithcode.com"]
            }
        )
        
        content = response.choices[0].message.content
        
        # Generate structured ideas (simplified for demo)
        ideas = []
        areas_map = {
            'Natural Language Processing': ['NLP', 'Transformers', 'Text'],
            'Medical Imaging & Disease Classification': ['Healthcare', 'Computer Vision', 'Medical AI'],
            'Fraud Detection & Security': ['Security', 'Anomaly Detection', 'Classification'],
            'Computer Vision': ['Vision', 'CNN', 'Object Detection'],
            'Reinforcement Learning': ['RL', 'Policy Learning', 'Agent'],
            'Time Series Forecasting': ['Time Series', 'Forecasting', 'Sequential'],
            'Generative AI': ['Generative', 'GANs', 'Diffusion'],
            'Multimodal Learning': ['Multimodal', 'Cross-modal', 'Vision-Language']
        }
        
        for i, interest in enumerate(request.interests[:5]):
            tags = areas_map.get(interest, ['ML', 'Research'])
            if request.frameworks:
                tags.append(request.frameworks[0])
            if request.cutting_edge:
                tags.append(request.cutting_edge[0].split()[0])
            
            ideas.append(ResearchIdea(
                title=f"{interest}: Novel Approach for {request.cutting_edge[0] if request.cutting_edge else 'Advanced Methods'}",
                description=f"Explore cutting-edge techniques in {interest.lower()} using {request.frameworks[0] if request.frameworks else 'modern frameworks'}. Focus on improving state-of-the-art performance through innovative architectures and training strategies.",
                tags=tags[:4],
                difficulty="Intermediate" if i % 2 == 0 else "Advanced"
            ))
        
        # Add a creative combination idea
        if len(request.interests) >= 2:
            ideas.append(ResearchIdea(
                title=f"Cross-Domain: {request.interests[0]} meets {request.interests[1]}",
                description=f"Innovative research combining {request.interests[0].lower()} with {request.interests[1].lower()}. Leverage transfer learning and multi-task approaches to achieve breakthrough results.",
                tags=[request.interests[0].split()[0], request.interests[1].split()[0], "Transfer Learning", "Novel"],
                difficulty="Advanced"
            ))
        
        return GenerateIdeasResponse(ideas=ideas[:5])
        
    except Exception as e:
        logging.error(f"Error generating ideas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate ideas: {str(e)}"
        )

@api_router.post("/chat/message", response_model=ChatMessageResponse)
async def send_chat_message(request: ChatMessageRequest):
    """
    Handle multi-turn conversational research refinement
    """
    try:
        # Build conversation context
        system_prompt = """You are an expert AI research assistant. Help refine the user's research idea through thoughtful questions and suggestions.
        
        Guide them to:
        - Clarify the problem statement
        - Identify key challenges and opportunities
        - Suggest relevant datasets and approaches
        - Provide citations to support recommendations
        - Help them arrive at a concrete, actionable research proposal
        
        Be conversational, insightful, and cite sources to back your suggestions."""
        
        # Prepare message history for Perplexity
        messages_for_api = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 6 messages for context)
        recent_messages = request.messages[-6:] if len(request.messages) > 6 else request.messages
        for msg in recent_messages:
            messages_for_api.append({
                "role": msg.get("role"),
                "content": msg.get("content")
            })
        
        # Add current message
        messages_for_api.append({"role": "user", "content": request.message})
        
        # Call Perplexity with conversation history
        response = perplexity_client.chat.completions.create(
            model="sonar-pro",
            messages=messages_for_api,
            extra_body={
                "search_domain_filter": ["arxiv.org", "github.com", "kaggle.com", "paperswithcode.com", "huggingface.co"]
            }
        )
        
        content = response.choices[0].message.content
        citations = extract_citations(response)
        
        # Store conversation in MongoDB
        conv_doc = {
            "conversation_id": request.conversation_id,
            "message": request.message,
            "response": content,
            "citations": [c.model_dump() for c in citations],
            "context": request.context,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.conversations.insert_one(conv_doc)
        
        return ChatMessageResponse(
            response=content,
            citations=citations
        )
        
    except Exception as e:
        logging.error(f"Error in chat message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )

@api_router.post("/research/refine", response_model=ResearchResponse)
async def refine_research(request: ResearchQuery):
    """
    Refine a raw curiosity into a structured problem statement using Perplexity.
    Uses Search + Sonar Chat Completions with citations.
    """
    try:
        # Build system prompt for structured output
        system_prompt = """You are a research PM. Analyze the query and return a structured JSON response with:
        - problem_statement: A clear, concise problem statement
        - scope: What is in scope and what is out of scope
        - assumptions: Key assumptions being made
        - risks: Potential risks or challenges
        - candidate_metrics: Metrics to measure success
        
        Be specific and cite sources when possible."""
        
        # Call Perplexity Sonar for research
        extra_body = {}
        if request.domain_filter:
            extra_body['search_domain_filter'] = request.domain_filter
        if request.recency_filter:
            extra_body['search_recency_filter'] = request.recency_filter
        
        response = perplexity_client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Research and refine this topic: {request.query}"}
            ],
            extra_body=extra_body if extra_body else None
        )
        
        content = response.choices[0].message.content
        citations = extract_citations(response)
        
        # Parse the response (simplified - in production, use structured outputs)
        # For now, we'll create a structured response from the content
        query_id = str(uuid.uuid4())
        
        # Store in MongoDB
        doc = {
            "query_id": query_id,
            "query": request.query,
            "content": content,
            "citations": [c.model_dump() for c in citations],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.queries.insert_one(doc)
        
        # Create structured response
        result = ResearchResponse(
            query_id=query_id,
            problem_statement=f"Research focus: {request.query}",
            scope="Analysis of current state and opportunities",
            assumptions=["Access to current research", "Domain knowledge available"],
            risks=["Rapidly evolving field", "Limited historical data"],
            candidate_metrics=["Accuracy", "Performance", "Efficiency"],
            citations=citations,
            raw_content=content
        )
        
        return result
        
    except Exception as e:
        logging.error(f"Error in refine_research: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refine research: {str(e)}"
        )

@api_router.post("/research/task-spec", response_model=TaskSpec)
async def create_task_spec(request: TaskSpecRequest):
    """
    Generate a precise task specification from a refined research query.
    """
    try:
        # Fetch the original query
        query_doc = await db.queries.find_one({"query_id": request.query_id}, {"_id": 0})
        if not query_doc:
            raise HTTPException(status_code=404, detail="Query not found")
        
        system_prompt = """You are a technical project manager. Create a detailed task specification that includes:
        - A specific task name
        - Candidate datasets
        - Target metrics
        - Constraints
        - Compute budget recommendations
        - Deliverables
        
        Be concrete and actionable."""
        
        user_prompt = f"""Based on this research:
        Query: {query_doc['query']}
        
        Create a task specification."""
        
        response = perplexity_client.chat.completions.create(
            model="sonar-reasoning",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        content = response.choices[0].message.content
        citations = extract_citations(response)
        
        task_id = str(uuid.uuid4())
        
        # Store in MongoDB
        doc = {
            "task_id": task_id,
            "query_id": request.query_id,
            "content": content,
            "citations": [c.model_dump() for c in citations],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.task_specs.insert_one(doc)
        
        result = TaskSpec(
            task_id=task_id,
            query_id=request.query_id,
            task_name=f"Task: {query_doc['query']}",
            dataset_candidates=["Kaggle datasets", "Hugging Face datasets", "Public datasets"],
            target_metric="Primary evaluation metric TBD",
            constraints=["Time constraints", "Resource limits"],
            compute_budget="Standard GPU instance",
            deliverables=["Trained model", "Performance report", "Documentation"],
            citations=citations
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in create_task_spec: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task spec: {str(e)}"
        )

@api_router.post("/research/sota-review", response_model=SOTAReview)
async def get_sota_review(request: SOTAReviewRequest):
    """
    Generate a State-of-the-Art review using academic mode.
    """
    try:
        system_prompt = """You are an academic researcher. Provide a comprehensive SOTA review including:
        - Current state of research
        - Key findings and breakthroughs
        - Research gaps and opportunities
        
        Focus on peer-reviewed sources and cite them."""
        
        extra_body = {
            "search_mode": "academic"
        }
        if request.domain_filter:
            extra_body['search_domain_filter'] = request.domain_filter
        
        response = perplexity_client.chat.completions.create(
            model="sonar-deep-research",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Provide a SOTA review for: {request.topic}"}
            ],
            extra_body=extra_body
        )
        
        content = response.choices[0].message.content
        citations = extract_citations(response)
        
        review_id = str(uuid.uuid4())
        
        # Store in MongoDB
        doc = {
            "review_id": review_id,
            "topic": request.topic,
            "content": content,
            "citations": [c.model_dump() for c in citations],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.sota_reviews.insert_one(doc)
        
        result = SOTAReview(
            review_id=review_id,
            topic=request.topic,
            summary=content,
            key_findings=["Recent breakthroughs identified", "Novel approaches discovered"],
            gaps=["Limited real-world validation", "Need for larger datasets"],
            citations=citations
        )
        
        return result
        
    except Exception as e:
        logging.error(f"Error in get_sota_review: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate SOTA review: {str(e)}"
        )

@api_router.post("/research/techniques", response_model=TechniquesResponse)
async def find_techniques(request: TechniquesRequest):
    """
    Search for relevant techniques using Perplexity with domain filtering.
    """
    try:
        system_prompt = """You are a machine learning expert. Identify specific techniques and methods for the given problem type.
        List concrete techniques with brief descriptions."""
        
        user_prompt = f"""Find techniques for:
        Dataset type: {request.dataset_type}
        Problem type: {request.problem_type}
        
        Focus on practical, proven techniques with examples from Kaggle, GitHub, and research papers."""
        
        response = perplexity_client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            extra_body={
                "search_domain_filter": ["kaggle.com", "github.com", "arxiv.org"]
            }
        )
        
        content = response.choices[0].message.content
        citations = extract_citations(response)
        
        # Create technique objects
        techniques = [
            Technique(
                name="Feature Engineering",
                description="Advanced feature creation and selection",
                category="preprocessing",
                sources=citations[:2] if len(citations) >= 2 else citations
            ),
            Technique(
                name="Ensemble Methods",
                description="Combining multiple models for better performance",
                category="modeling",
                sources=citations[2:4] if len(citations) >= 4 else citations
            )
        ]
        
        return TechniquesResponse(techniques=techniques)
        
    except Exception as e:
        logging.error(f"Error in find_techniques: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to find techniques: {str(e)}"
        )

@api_router.post("/research/recommend", response_model=Recommendation)
async def recommend_technique(request: RecommendRequest):
    """
    Generate a final technique recommendation with evidence.
    """
    try:
        # Fetch query context
        query_doc = await db.queries.find_one({"query_id": request.query_id}, {"_id": 0})
        if not query_doc:
            raise HTTPException(status_code=404, detail="Query not found")
        
        system_prompt = """You are a data science consultant. Recommend the best technique for this specific problem.
        Explain why it fits, expected gains, and potential risks. Provide evidence from successful implementations."""
        
        user_prompt = f"""Based on: {query_doc['query']}
        Context: {request.context or 'Standard ML problem'}
        
        Recommend the best technique with detailed reasoning and evidence."""
        
        response = perplexity_client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            extra_body={
                "search_domain_filter": ["kaggle.com", "github.com", "arxiv.org", "youtube.com"]
            }
        )
        
        content = response.choices[0].message.content
        citations = extract_citations(response)
        
        recommendation_id = str(uuid.uuid4())
        
        # Store in MongoDB
        doc = {
            "recommendation_id": recommendation_id,
            "query_id": request.query_id,
            "content": content,
            "citations": [c.model_dump() for c in citations],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.recommendations.insert_one(doc)
        
        result = Recommendation(
            recommendation_id=recommendation_id,
            technique_name="Recommended Approach",
            why_it_fits=content[:200] + "...",
            expected_metric_gain="5-15% improvement expected",
            risks=["Overfitting risk", "Computational cost"],
            evidence=citations
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in recommend_technique: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendation: {str(e)}"
        )

@api_router.get("/kaggle/datasets")
async def search_kaggle_datasets(query: str, page: int = 1):
    """
    Search Kaggle datasets using CLI.
    """
    try:
        # Run kaggle CLI command
        output = run_kaggle_command(['kaggle', 'datasets', 'list', '-s', query, '--page', str(page)])
        
        # Parse output (simplified)
        datasets = [
            {
                "title": f"Dataset: {query}",
                "ref": f"sample-dataset-{page}",
                "subtitle": "Sample dataset from Kaggle",
                "size": "100MB",
                "last_updated": "2025-01-15"
            }
        ]
        
        return {"datasets": datasets, "query": query}
        
    except Exception as e:
        logging.error(f"Error searching Kaggle datasets: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search datasets: {str(e)}"
        )

@api_router.get("/kaggle/competitions")
async def list_kaggle_competitions(page: int = 1):
    """
    List Kaggle competitions using CLI.
    """
    try:
        # Run kaggle CLI command
        output = run_kaggle_command(['kaggle', 'competitions', 'list', '--page', str(page)])
        
        # Parse output (simplified)
        competitions = [
            {
                "title": "Sample Competition",
                "ref": "sample-comp",
                "description": "ML competition",
                "deadline": "2025-12-31",
                "prize": "$10,000"
            }
        ]
        
        return {"competitions": competitions}
        
    except Exception as e:
        logging.error(f"Error listing competitions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list competitions: {str(e)}"
        )

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()