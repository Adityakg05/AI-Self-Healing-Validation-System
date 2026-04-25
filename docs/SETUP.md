# Quick Start Guide

I made the setup process as simple as possible. You just need Python and a few API keys.

## 1. Prerequisites
- Python 3.10+
- A Groq or Gemini API Key
- A GitHub Personal Access Token (for PR creation)

## 2. Installation
```bash
# Clone and install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Open .env and add your keys
```

## 3. Running the Project
I built a `run_all.py` script that launches both the monitored app and the agent dashboard at the same time:

```bash
python run_all.py
```

### Testing the Healing Loop
1. Open the Streamlit dashboard (usually `http://localhost:8501`).
2. Use the "Trigger Crash" button.
3. Watch the logs in the terminal or dashboard to see the agents start the repair.
4. Check your GitHub for the new Pull Request!
