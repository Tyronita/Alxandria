from fastapi import FastAPI, APIRouter, HTTPException, status
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
from openai import OpenAI
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Perplexity client
perplexity_client = OpenAI(
    api_key=os.environ.get('PERPLEXITY_API_KEY'),
    base_url="https://api.perplexity.ai"
)

app = FastAPI(title="Research Blueprint API")
api_router = APIRouter(prefix="/api")

# ============ MODELS ============

class Citation(BaseModel):
    title: str
    url: str
    snippet: Optional[str] = None

class ResearchPaper(BaseModel):
    title: str
    authors: str
    contribution: str
    paper_url: str
    code_url: Optional[str] = None

class ResearchGap(BaseModel):
    title: str
    problem: str
    solution: str
    impact: str
    libraries: List[str]

class DatasetInfo(BaseModel):
    name: str
    size: str
    format: str
    source: str
    sota_metrics: Dict[str, Any]
    access_links: Dict[str, str]

class BlueprintStage(BaseModel):
    stage: str  # 'curiosity', 'research', 'gaps', 'dataset', 'implementation'
    completed: bool
    data: Dict[str, Any]

class ChatConverseRequest(BaseModel):
    session_id: str
    message: str
    is_initial: bool = False
    conversation_history: List[Dict[str, Any]] = []

class ChatConverseResponse(BaseModel):
    response: str
    citations: List[Citation] = []
    blueprint_update: Optional[Dict[str, Any]] = None
    show_blueprint: bool = False

# ============ HELPERS ============

def extract_citations(response) -> List[Citation]:
    """Extract citations from Perplexity response"""
    citations = []
    if hasattr(response, 'citations'):
        for i, url in enumerate(response.citations or []):
            citations.append(Citation(
                title=f"Source {i+1}",
                url=url,
                snippet=""
            ))
    return citations

def detect_blueprint_stage(message: str, conversation_history: List) -> str:
    """Detect what stage of blueprint creation we're at"""
    message_lower = message.lower()
    history_text = " ".join([m.get('content', '').lower() for m in conversation_history[-3:]])
    
    # Stage detection logic
    if any(word in message_lower for word in ['want to learn', 'interested in', 'curious about']):
        return 'curiosity'
    elif any(word in history_text for word in ['papers', 'research', 'literature', 'state of the art']):
        return 'papers'
    elif any(word in history_text for word in ['gaps', 'opportunities', 'novel', 'future directions']):
        return 'gaps'
    elif any(word in message_lower + history_text for word in ['dataset', 'data', 'benchmark']):
        return 'dataset'
    elif any(word in message_lower + history_text for word in ['implement', 'code', 'build', 'ready']):
        return 'implementation'
    
    return 'unknown'

# ============ ROUTES ============

@api_router.get("/")
async def root():
    return {"message": "Research Blueprint API", "version": "2.0.0"}

@api_router.post("/chat/converse", response_model=ChatConverseResponse)
async def conversational_research(request: ChatConverseRequest):
    """
    Guided conversational research that builds comprehensive blueprints
    """
    try:
        # Detect blueprint stage
        stage = detect_blueprint_stage(request.message, request.conversation_history)
        
        # Build system prompt based on stage
        if stage == 'curiosity':
            system_prompt = """You are a research mentor. The user just shared their curiosity. Your job:

1. ACKNOWLEDGE their interest warmly
2. ASK clarifying questions to understand depth (beginner vs advanced)
3. SUGGEST exploring: relevant papers, current research gaps, and available datasets
4. GUIDE them to the next step: "Would you like me to find the top 3 research papers in this area?"

Be conversational and encouraging."""
        
        elif stage == 'papers':
            system_prompt = """You are a research librarian. Find the 3 MOST RELEVANT papers for their topic.

For EACH paper, provide:
- Title and authors
- Key contribution (1 sentence)
- Link to paper (arxiv/IEEE/ACL)
- Link to code repository if available (GitHub)

Format as a markdown table. Then ask: "Would you like me to identify research gaps and novel opportunities?"

Use search to find actual papers with working links."""
        
        elif stage == 'gaps':
            system_prompt = """You are a research strategist. Identify 2-3 SPECIFIC research gaps.

For EACH gap:
- **Title**: Concise gap name
- **Problem**: What's missing in current work
- **Solution**: Specific approach to address it
- **Impact**: Expected improvement (quantitative if possible)
- **Libraries**: Python packages needed

Be specific and actionable. Then ask: "Ready to find the best dataset for this?"""
        
        elif stage == 'dataset':
            system_prompt = """You are a dataset curator. Find the BEST dataset for their research.

Provide:
- Dataset name and source
- Size and format
- Current SOTA performance (table with metric/score/method/year)
- Access links (Kaggle, HuggingFace, official site)

Use search to find real datasets with benchmarks. Format SOTA as markdown table.

Then ask: "Shall I create your implementation checklist?"""
        
        elif stage == 'implementation':
            system_prompt = """You are a technical implementation guide. Create a detailed checklist.

Provide:
1. **Requirements.txt**: All Python packages needed
2. **Component Status Table**: 
   - Component | Status (✅/⚠️/❌) | Notes
3. **Next Steps**: Prioritized TODO list

Be comprehensive. Include data loading, model baseline, metrics, and gap implementations.

End with: "Would you like me to show you starter code for the baseline?"""
        
        else:
            system_prompt = """You are an expert AI research guide. 

Guide the user through creating a comprehensive research blueprint:
1. Understand curiosity
2. Find relevant papers  
3. Identify research gaps
4. Select optimal dataset
5. Create implementation plan

Ask thoughtful questions. Provide citations. Be encouraging."""
        
        # Build messages
        messages_to_send = [{"role": "system", "content": system_prompt}]
        
        # Add history
        for msg in request.conversation_history[-6:]:
            if msg.get("role") in ["user", "assistant"]:
                messages_to_send.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Add current message
        messages_to_send.append({"role": "user", "content": request.message})
        
        # Call Perplexity
        response = perplexity_client.chat.completions.create(
            model="sonar-pro",
            messages=messages_to_send,
            extra_body={
                "search_domain_filter": [
                    "arxiv.org", "github.com", "kaggle.com", 
                    "paperswithcode.com", "huggingface.co",
                    "ieeexplore.ieee.org", "aclanthology.org"
                ]
            }
        )
        
        content = response.choices[0].message.content
        citations = extract_citations(response)
        
        # Store conversation
        conv_doc = {
            "session_id": request.session_id,
            "message": request.message,
            "response": content,
            "stage": stage,
            "citations": [c.model_dump() for c in citations],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.conversations.insert_one(conv_doc)
        
        # Check if we should show blueprint
        show_blueprint = stage in ['dataset', 'implementation']
        
        return ChatConverseResponse(
            response=content,
            citations=citations,
            show_blueprint=show_blueprint
        )
        
    except Exception as e:
        logging.error(f"Error in conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process conversation: {str(e)}"
        )

@api_router.post("/blueprint/generate")
async def generate_full_blueprint(session_id: str):
    """
    Generate complete research blueprint from conversation history
    """
    try:
        # Fetch conversation
        conversations = await db.conversations.find(
            {"session_id": session_id}
        ).sort("timestamp", 1).to_list(100)
        
        if not conversations:
            raise HTTPException(status_code=404, detail="No conversation found")
        
        # Extract all AI responses
        full_context = "\n\n".join([
            conv['response'] for conv in conversations 
            if 'response' in conv
        ])
        
        # Generate structured blueprint
        system_prompt = """You are a research blueprint generator. 

Given conversation history, create a COMPLETE research blueprint in this EXACT format:

```markdown
# 👤 Research Project: [Title]

## Curiosity Statement
> "[User's original interest]"

## 📚 3 Most Relevant Research Papers

| # | Paper | Key Contribution | Resources |
|---|-------|------------------|-----------|
| 1 | [Title] ([Authors], [Venue Year]) | [Contribution] | [Paper](url) · [Code](url) |
...

## 💡 Research Gaps / Future Directions

### Gap 1: **[Title]**
**Problem:** [Description]
**Solution:** [Approach]
**Impact:** [Expected improvement]
**Libraries:** `lib1`, `lib2`

## 📊 Dataset: [Name]

### Dataset Info
- **Source:** [Organization]
- **Size:** [Numbers]
- **Format:** [File types]

### Current Best KPIs

| Metric | Best Score | Method | Year |
|--------|------------|--------|------|
...

### Access Links
- **Kaggle:** [url]
- **HuggingFace:** [url]

## ✅ IMPLEMENTATION CHECKLIST

### 📦 Requirements.txt
```txt
[packages]
```

### Status Table

| Component | Status | Notes |
|-----------|--------|-------|
| Dataset Import | ✅ COMPLETE | HF loader |
...

## 📋 NEXT STEPS
- [ ] [Task 1]
- [ ] [Task 2]
```

Use the conversation to fill in ALL details. Be comprehensive and structured."""
        
        response = perplexity_client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create blueprint from:\n\n{full_context}"}
            ]
        )
        
        blueprint = response.choices[0].message.content
        
        # Store blueprint
        blueprint_doc = {
            "session_id": session_id,
            "blueprint": blueprint,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        await db.blueprints.insert_one(blueprint_doc)
        
        return {"blueprint": blueprint}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error generating blueprint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate blueprint: {str(e)}"
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