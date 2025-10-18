from fastapi import FastAPI, APIRouter, HTTPException, status
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from openai import OpenAI
import json
import subprocess
import tempfile

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Perplexity
perplexity_client = OpenAI(
    api_key=os.environ.get('PERPLEXITY_API_KEY'),
    base_url="https://api.perplexity.ai"
)

# Kaggle
kaggle_username = os.environ.get('KAGGLE_USERNAME')
kaggle_key = os.environ.get('KAGGLE_KEY')

app = FastAPI(title="Alexandria API")
api_router = APIRouter(prefix="/api")

# ============ MODELS ============

class Citation(BaseModel):
    title: str
    url: str

class ChatRequest(BaseModel):
    session_id: str
    message: str
    conversation_history: List[Dict[str, Any]] = []

class ChatResponse(BaseModel):
    response: str
    citations: List[Citation] = []

# ============ HELPERS ============

def extract_citations(response) -> List[Citation]:
    citations = []
    if hasattr(response, 'citations') and response.citations:
        for i, url in enumerate(response.citations):
            citations.append(Citation(title=f"[{i+1}]", url=url))
    return citations

def run_kaggle_command(command: List[str]) -> str:
    """Run kaggle CLI with credentials"""
    kaggle_config = {
        "username": kaggle_username,
        "key": kaggle_key
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(kaggle_config, f)
        temp_file = f.name
    
    try:
        env = os.environ.copy()
        env['KAGGLE_USERNAME'] = kaggle_username
        env['KAGGLE_KEY'] = kaggle_key
        
        result = subprocess.run(command, capture_output=True, text=True, env=env)
        return result.stdout
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

# ============ ROUTES ============

@api_router.get("/")
async def root():
    return {"message": "Alexandria API", "version": "3.0.0"}

@api_router.post("/research/complete", response_model=ChatResponse)
async def complete_research(request: ChatRequest):
    """
    Complete end-to-end research using Perplexity:
    1. Find relevant papers
    2. Identify research gaps
    3. Select best dataset (with Kaggle links)
    4. Provide implementation plan
    """
    try:
        # Build comprehensive research prompt
        system_prompt = """You are Alexandria, an AI research assistant. Given a research topic, provide:

## 1. Top 3 Research Papers
Find the 3 most relevant papers. For each:
- Title and authors
- Key contribution
- Paper link (arxiv/IEEE)
- Code link (GitHub if available)

Format as markdown table.

## 2. Research Gaps (2-3)
For each gap:
- **Gap Title**
- **Problem**: What's missing
- **Solution**: How to address it
- **Impact**: Expected improvement

## 3. Best Dataset
Identify THE BEST dataset for this research:
- Dataset name and source
- Size and format  
- **Kaggle Competition Link** (if exists)
- **Current SOTA**: Table with Metric | Score | Method | Year
- Access links (Kaggle, HuggingFace, official)

## 4. Implementation Checklist
- Required Python packages
- Key components to build
- Next steps

Be specific. Use real links. Format with markdown tables."""
        
        # Get conversation history
        history_text = "\n".join([
            f"{msg.get('role')}: {msg.get('content')}"
            for msg in request.conversation_history[-4:]
        ])
        
        user_prompt = f"""Research Topic: {request.message}

Previous Context:
{history_text}

Provide complete research analysis."""
        
        # Call Perplexity
        response = perplexity_client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            extra_body={
                "search_domain_filter": [
                    "arxiv.org", "github.com", "kaggle.com",
                    "paperswithcode.com", "huggingface.co"
                ]
            }
        )
        
        content = response.choices[0].message.content
        citations = extract_citations(response)
        
        # Store in DB
        doc = {
            "session_id": request.session_id,
            "message": request.message,
            "response": content,
            "citations": [c.model_dump() for c in citations],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.research.insert_one(doc)
        
        return ChatResponse(
            response=content,
            citations=citations
        )
        
    except Exception as e:
        logging.error(f"Research error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Research failed: {str(e)}"
        )

@api_router.get("/kaggle/dataset/{dataset_name}")
async def get_kaggle_dataset_info(dataset_name: str):
    """
    Get Kaggle dataset info and leaderboard
    """
    try:
        # Get dataset files
        output = run_kaggle_command(['kaggle', 'datasets', 'files', '-d', dataset_name])
        
        return {
            "dataset": dataset_name,
            "files": output,
            "download_command": f"kaggle datasets download -d {dataset_name}"
        }
    except Exception as e:
        logging.error(f"Kaggle error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/kaggle/competition/{competition}")
async def get_kaggle_competition(competition: str):
    """
    Get Kaggle competition leaderboard
    """
    try:
        output = run_kaggle_command(['kaggle', 'competitions', 'leaderboard', competition, '--show'])
        
        return {
            "competition": competition,
            "leaderboard": output,
            "submit_command": f"kaggle competitions submit -c {competition} -f submission.csv -m 'Submission'"
        }
    except Exception as e:
        logging.error(f"Competition error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()