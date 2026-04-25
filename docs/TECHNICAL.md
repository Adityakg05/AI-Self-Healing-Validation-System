# Technical Details

I built this project to experiment with stateful AI agents. Here are the three most interesting technical challenges I solved:

## 🔄 Self-Correction Logic
The system doesn't just try once. If the **Validator** finds a syntax error or a bug, it passes the error message back to the **Mechanic**. This feedback loop allows the agent to learn from its own mistakes in real-time.

## 💾 LangGraph State Management
I used a `TypedDict` to manage the "brain" of the project. By using the **reducer pattern** (Annotated add), I can append message history automatically, which gives the agents a "memory" of what they've already tried.

## 🛡️ AST-Based Validation
Instead of running the AI code directly (which is dangerous), I used Python's **Abstract Syntax Tree (AST)** module to verify that the code is syntactically correct before it's ever submitted to GitHub.

---
*This implementation proved that AI agents are most effective when they have a deterministic validation layer checking their work.*
