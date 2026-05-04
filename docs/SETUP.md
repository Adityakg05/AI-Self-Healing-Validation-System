# Setup Guide

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Environment Variables
Copy `.env.example` to `.env` and add:
- `GROQ_API_KEY` or `GEMINI_API_KEY`
- `GITHUB_TOKEN` (for PRs)
- `GITHUB_REPO` (your username/repo)

## 3. Launch everything
Run the all-in-one script:
```bash
python run_all.py
```

Open the Streamlit URL to see the dashboard. You can trigger a crash from there to see the agent in action.
