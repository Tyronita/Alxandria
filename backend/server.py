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

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

perplexity_client = OpenAI(
    api_key=os.environ.get('PERPLEXITY_API_KEY'),
    base_url="https://api.perplexity.ai"
)

kaggle_username = os.environ.get('KAGGLE_USERNAME')
kaggle_key = os.environ.get('KAGGLE_KEY')

app = FastAPI(title="Alexandria API")
api_router = APIRouter(prefix="/api")

# ============ MODELS ============

class Citation(BaseModel):
    title: str
    url: str

class StepRequest(BaseModel):
    session_id: str
    topic: str
    step: int
    selected_data: Optional[Dict[str, Any]] = None

class StepResponse(BaseModel):
    step: int
    content: str
    citations: List[Citation] = []
    options: Optional[List[Dict[str, Any]]] = None
    next_step_available: bool = False

# ============ HELPERS ============

def extract_citations(response) -> List[Citation]:
    citations = []
    if hasattr(response, 'citations') and response.citations:
        for i, url in enumerate(response.citations):
            citations.append(Citation(title=f"[{i+1}]", url=url))
    return citations

def run_kaggle_command(command: List[str]) -> str:
    kaggle_config = {"username": kaggle_username, "key": kaggle_key}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(kaggle_config, f)
        temp_file = f.name
    
    try:
        env = os.environ.copy()
        env['KAGGLE_USERNAME'] = kaggle_username
        env['KAGGLE_KEY'] = kaggle_key
        result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=30)
        return result.stdout
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

# ============ ROUTES ============

@api_router.get("/")
async def root():
    return {"message": "Alexandria API", "version": "4.0.0"}

@api_router.post("/research/step", response_model=StepResponse)
async def research_step(request: StepRequest):
    """
    Multi-step research journey
    Step 1: Papers & Full Analysis
    Step 2: Research Gaps  
    Step 3: Dataset Options (user selects)
    Step 4: Implementation Plan
    Step 5: Kaggle Setup
    """
    try:
        if request.step == 1:
            # STEP 1: Papers & Full Analysis
            system_prompt = """You are Alexandria. Provide comprehensive analysis:

## Top 3 Research Papers
| # | Paper | Authors | Contribution | Links |
|---|-------|---------|--------------|-------|
| 1 | [Title] | [Authors] | [Key insight] | [Paper](url) · [Code](url) |

For EACH paper, include working arxiv/github links.

## Full Area Analysis
Provide deep analysis:
- **Current State**: What's the SOTA? What methods dominate?
- **Key Challenges**: What problems remain unsolved?
- **Recent Breakthroughs**: Major advances in last 2 years
- **Performance Benchmarks**: Typical accuracy/metrics achieved

Be comprehensive. Use real data from search."""
            
            response = perplexity_client.chat.completions.create(
                model="sonar-pro",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Research topic: {request.topic}"}
                ],
                extra_body={"search_domain_filter": ["arxiv.org", "github.com", "paperswithcode.com"]}
            )
            
            content = response.choices[0].message.content
            citations = extract_citations(response)
            
            await db.research.insert_one({
                "session_id": request.session_id,
                "step": 1,
                "topic": request.topic,
                "content": content,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
            return StepResponse(
                step=1,
                content=content,
                citations=citations,
                next_step_available=True
            )
        
        elif request.step == 2:
            # STEP 2: Research Gaps
            system_prompt = """You are Alexandria. Identify specific research gaps:

## Research Gaps & Opportunities

For each gap (2-3 total):

### Gap 1: **[Specific Gap Title]**
- **Problem**: Detailed problem description
- **Current Limitations**: What methods fail at
- **Proposed Solution**: Novel approach to address it
- **Expected Impact**: Quantitative improvement estimate
- **Difficulty**: Beginner/Intermediate/Advanced

Be specific and actionable."""
            
            response = perplexity_client.chat.completions.create(
                model="sonar-pro",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Find research gaps for: {request.topic}"}
                ],
                extra_body={"search_domain_filter": ["arxiv.org", "paperswithcode.com"]}
            )
            
            content = response.choices[0].message.content
            citations = extract_citations(response)
            
            await db.research.update_one(
                {"session_id": request.session_id, "step": 1},
                {"$set": {"gaps": content}}
            )
            
            return StepResponse(
                step=2,
                content=content,
                citations=citations,
                next_step_available=True
            )
        
        elif request.step == 3:
            # STEP 3: Dataset Options
            system_prompt = """You are Alexandria. Find 3-4 dataset options:

## Dataset Options

For EACH dataset:

### Dataset 1: [Name]
- **Source**: Kaggle/HuggingFace/Official
- **Size**: Number of samples, file size
- **Format**: Image/Text/Tabular, file types
- **Difficulty**: Easy/Medium/Hard
- **SOTA Performance**: Best reported score
- **Kaggle Competition**: Yes/No (include link if yes)
- **Access**: Direct download link

Provide working links. Include Kaggle competitions if they exist."""
            
            response = perplexity_client.chat.completions.create(
                model="sonar-pro",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Find datasets for: {request.topic}"}
                ],
                extra_body={"search_domain_filter": ["kaggle.com", "huggingface.co", "paperswithcode.com"]}
            )
            
            content = response.choices[0].message.content
            citations = extract_citations(response)
            
            # Parse dataset options (simplified)
            options = [
                {"id": 1, "name": "Dataset 1", "description": "Primary option"},
                {"id": 2, "name": "Dataset 2", "description": "Alternative"},
                {"id": 3, "name": "Dataset 3", "description": "Backup option"}
            ]
            
            await db.research.update_one(
                {"session_id": request.session_id, "step": 1},
                {"$set": {"datasets": content}}
            )
            
            return StepResponse(
                step=3,
                content=content,
                citations=citations,
                options=options,
                next_step_available=False  # Wait for selection
            )
        
        elif request.step == 4:
            # STEP 4: Implementation Plan (after dataset selection)
            selected_dataset = request.selected_data.get('dataset_name', 'selected dataset') if request.selected_data else 'selected dataset'
            
            system_prompt = f"""You are Alexandria. Create implementation plan for {selected_dataset}:

## Implementation Checklist

### 1. Environment Setup
```txt
# requirements.txt
[List all packages]
```

### 2. Data Pipeline
- [ ] Download dataset
- [ ] Data preprocessing
- [ ] Train/val/test split
- [ ] Data augmentation

### 3. Model Architecture
- [ ] Baseline model selection
- [ ] Model implementation
- [ ] Training loop

### 4. Evaluation
- [ ] Metrics implementation
- [ ] Validation strategy
- [ ] Benchmarking

### 5. Current SOTA Benchmark
| Metric | Score | Method | Year |
|--------|-------|--------|------|
[Fill with real data]

Be specific and comprehensive."""
            
            response = perplexity_client.chat.completions.create(
                model="sonar-pro",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Implementation plan for {request.topic} using {selected_dataset}"}
                ],
                extra_body={"search_domain_filter": ["github.com", "paperswithcode.com"]}
            )
            
            content = response.choices[0].message.content
            citations = extract_citations(response)
            
            await db.research.update_one(
                {"session_id": request.session_id, "step": 1},
                {"$set": {"implementation": content, "selected_dataset": selected_dataset}}
            )
            
            return StepResponse(
                step=4,
                content=content,
                citations=citations,
                next_step_available=True
            )
        
        elif request.step == 5:
            # STEP 5: Kaggle Setup & Notebook
            selected_dataset = request.selected_data.get('dataset_name', 'dataset')
            
            # Get Kaggle competition info if available
            kaggle_info = ""
            try:
                if 'kaggle.com/c/' in selected_dataset:
                    comp_name = selected_dataset.split('/c/')[-1].split('/')[0]
                    leaderboard = run_kaggle_command(['kaggle', 'competitions', 'leaderboard', comp_name, '--show'])
                    kaggle_info = f"\n## Kaggle Leaderboard\n```\n{leaderboard}\n```"
            except:
                pass
            
            system_prompt = f"""You are Alexandria. Final setup for Kaggle submission:

## Kaggle Setup Guide

### 1. Authentication
```bash
# Setup Kaggle credentials
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_key"
```

### 2. Download Dataset
```bash
kaggle datasets download -d [dataset-name]
```

### 3. Notebook Template
Provide starter notebook structure with:
- Data loading
- Baseline model
- Training loop
- Submission format

### 4. Submission Commands
```bash
kaggle competitions submit -c [competition] -f submission.csv -m "First submission"
```

{kaggle_info}

Make it copy-paste ready."""
            
            response = perplexity_client.chat.completions.create(
                model="sonar-pro",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Kaggle setup for {request.topic}"}
                ]
            )
            
            content = response.choices[0].message.content
            citations = extract_citations(response)
            
            await db.research.update_one(
                {"session_id": request.session_id, "step": 1},
                {"$set": {"kaggle_setup": content}}
            )
            
            return StepResponse(
                step=5,
                content=content,
                citations=citations,
                next_step_available=False  # Journey complete
            )
        
        else:
            raise HTTPException(status_code=400, detail="Invalid step")
            
    except Exception as e:
        logging.error(f"Step {request.step} error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Step failed: {str(e)}"
        )

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()