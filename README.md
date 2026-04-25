# AI Self-Healing SRE Agent

A simple but effective system that uses AI agents to find and fix bugs in a web application. Instead of just sending an alert, this tool investigates the logs and proposes a code fix automatically.

## ❓ The Problem
In many small projects, a simple bug (like a missing key in a dictionary) can crash a service and go unnoticed for hours. Manually checking logs and writing a fix is repetitive work. I wanted to see if I could automate this triage process using LLMs.

## 💡 Solution Overview
I built an agentic workflow that monitors application logs. When it detects a crash, it uses an "Investigator" agent to find the root cause and a "Mechanic" agent to write the fix. To make sure the AI doesn't make things worse, I added a "Validator" step that checks the code for errors before it ever gets submitted.

## ⚙️ How It Works
1. **Detection:** The system scans `app_logs.txt` for error messages.
2. **Analysis:** An AI agent looks at the stack trace to understand why the app crashed.
3. **Repair:** A second agent writes a surgical fix (like adding a `.get()` or a try/except).
4. **Validation:** The code is checked for syntax errors. If it fails, the agent tries again with the error feedback.
5. **Submission:** Once fixed, the system creates a Pull Request on GitHub.

## ✨ Key Features
- **Auto-Triage:** Automatically pulls the relevant error from messy logs.
- **Self-Correction:** If the first fix is broken, the agent learns from the error and tries again.
- **Safe Validation:** Checks the code for syntax issues before proposing a change.
- **GitHub Integration:** Automates the branching and PR process.
- **Live Monitoring:** Includes a Streamlit dashboard to see the agents working in real-time.

## 🛠️ Tech Stack
- **Python** (Core logic)
- **LangGraph** (Managing the agent workflow)
- **FastAPI** (The app being monitored)
- **Streamlit** (For the monitoring dashboard)
- **Groq / Gemini** (The AI brains)

## 🚀 How to Run
1. **Install:** `pip install -r requirements.txt`
2. **Setup:** Copy `.env.example` to `.env` and add your API keys.
3. **Start:** Run `python run_all.py` to launch the app and the dashboard.
4. **Test:** Trigger a bug from the dashboard and watch the healing loop start.

## 🔮 Future Improvements
- **Better Testing:** Move from simple syntax checks to running actual unit tests in a container.
- **Log Sources:** Connect to real monitoring tools like Datadog instead of local files.
- **Multi-File Fixes:** Expand the agent to handle bugs that span across multiple files.

## 📝 Personal Note
I built this project to explore how AI agents can handle real-world tasks like incident response. One challenge I faced was making sure the agent didn't get stuck in an infinite loop when it couldn't find a fix—adding iteration limits and validation feedback solved this.
