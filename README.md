#- Perplexity Hackathon Project

Video and Submission
https://devpost.com/software/alxandria

An AI-powered research assistant that transforms curiosity into structured research, complete with citations, task specifications, and actionable recommendations.

## 🌟 Features

### Core Research Capabilities
- **Research Refinement**: Transform raw queries into structured problem statements with Perplexity's Sonar models
- **Task Specifications**: Generate precise, actionable task specs with metrics and constraints
- **SOTA Reviews**: Access state-of-the-art research using academic search mode
- **Technique Discovery**: Find proven techniques from Kaggle, GitHub, and research papers
- **Evidence-Based Recommendations**: Get recommendations backed by citations and real-world examples
- **Kaggle Integration**: Explore datasets and competitions directly from the platform

### Powered By
- **Perplexity API**: Search API + Chat Completions (Sonar, Sonar-Pro, Sonar-Deep-Research, Sonar-Reasoning)
- **Kaggle API**: Dataset and competition exploration
- **MongoDB**: Research data persistence
- **React + FastAPI**: Modern full-stack architecture

## 🚀 Getting Started

### Install and Run
```bash
supervisorctl restart backend
supervisorctl restart frontend
```

### Process Logs
Backend Process: `/var/log/supervisor/backend.err.log` (or .out.log)
Frontend Process: `/var/log/supervisor/frontend.err.log` (or .out.log)

## 🎯 API Endpoints

- `POST /api/research/refine` - Refine research queries with Perplexity
- `POST /api/research/task-spec` - Generate task specifications
- `POST /api/research/sota-review` - Get SOTA reviews (academic mode)
- `POST /api/research/techniques` - Find techniques from Kaggle/GitHub
- `POST /api/research/recommend` - Get evidence-based recommendations
- `GET /api/kaggle/datasets` - Search Kaggle datasets
- `GET /api/kaggle/competitions` - List competitions

## 🏆 Built for Perplexity Hackathon 2025
