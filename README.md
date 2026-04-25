# 🤖 AI Self-Healing SRE Agent

A personal project exploring how AI agents can autonomously detect and fix production bugs. This system doesn't just alert you that something is broken; it identifies the root cause and opens a Pull Request with the fix.

> **The Elevator Pitch:** "I built an AI-powered SRE agent that autonomously fixes production bugs. When a crash occurs, it analyzes logs using LLMs, generates a Python fix, validates it through simulated tests, and if validation fails, it self-corrects by looping back with feedback—just like a human engineer would."

## ❓ The Problem
I wanted to see if I could automate the "boring" part of being an SRE: waking up at 2 AM to fix a simple `KeyError` or `TypeError` that crashed a service. Usually, these bugs take minutes to fix but hours of sleep are lost. I built this to see if an AI could handle the triage and repair loop on its own.

## 💡 Solution Overview
This agent acts as a "First Responder." It monitors application logs, uses a multi-agent workflow to investigate the crash, writes a Python fix, and validates it against the original code structure before submitting it for human review.

## ✨ Key Features
- **Auto-Investigation:** Reads raw logs to find the exact line and cause of a crash.
- **Self-Correction Loop:** If the first fix fails validation, the agent "re-thinks" and tries a different approach.
- **AST Validation:** Uses Python's Abstract Syntax Tree to ensure the AI doesn't break function signatures or introduce syntax errors.
- **GitOps Ready:** Automatically handles branching and Pull Request creation.
- **Real-time Dashboard:** A Streamlit UI to watch the agent's "thought process" as it works.

## 🏗️ Architecture Overview
I used **LangGraph** to build a stateful workflow. Instead of one big prompt, I split the logic into four distinct agents:
1. **Investigator:** Analyzes the logs.
2. **Mechanic:** Writes the code fix.
3. **Validator:** Tests the fix for syntax and logic errors.
4. **PR Creator:** Handles the GitHub integration.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Orchestration:** LangGraph (for the agent workflow)
- **Models:** Groq (Llama 3) or Google Gemini
- **Backend:** FastAPI (the service being monitored)
- **UI:** Streamlit

## ⚙️ How It Works
1. **Trigger:** A crash occurs in the FastAPI app and is logged to a file.
2. **Detection:** The Investigator Agent fetches the latest logs and identifies the crash.
3. **Fixing:** The Mechanic Agent generates a surgical fix for that specific error.
4. **Validation:** The Validator Node checks if the code is safe. If it fails, it sends feedback back to the Mechanic for a retry.
5. **PR:** Once validated, a Pull Request is opened on GitHub for the user to merge.

## 🚀 How to Run
1. **Install:** `pip install -r requirements.txt`
2. **Config:** Copy `.env.example` to `.env` and add your API keys.
3. **Start:** Run `python run_all.py` to launch both the app and the agent dashboard.
4. **Test:** Use the dashboard to trigger a crash and watch the healing loop start.

## 🛠️ Common Issues (Quick Fix)
- **"No LLM API key":** Ensure `GROQ_API_KEY` or `GEMINI_API_KEY` is in your `.env`.
- **"Port 8000 in use":** Kill the process running on 8000 or change the port in `app.py`.
- **"PR Creation failed":** Check your `GITHUB_TOKEN` permissions (it needs `repo` scope).

## 🔮 Future Improvements
- **Live Monitoring:** Connect to Datadog or CloudWatch instead of local logs.
- **Dockerized Tests:** Run the proposed fix in a temporary container to verify it actually passes unit tests.
- **Cost Controls:** Add more granular token tracking to optimize API spend.
- **Multi-File Support:** Expand the Mechanic's ability to fix bugs across multiple files.

---
---
*I built this to experiment with the boundaries of autonomous coding agents. It's a great demonstration of how AI can assist in incident response.*

### 📚 Further Reading
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/) | [Groq Cloud](https://console.groq.com/) | [FastAPI](https://fastapi.tiangolo.com/)
