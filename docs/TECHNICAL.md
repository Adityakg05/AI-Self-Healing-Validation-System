# Core Logic

This project helped me understand how to build reliable AI tools. Here are the three main technical parts:

## 1. The Validation Loop
The most interesting part was the feedback loop. If the "Validator" finds a syntax error, it doesn't just stop—it passes that error back to the agent. This allows the AI to "self-heal" its own code.

## 2. State Management
I used a `TypedDict` to pass data between agents. Each agent adds its work to the "State," so the next agent has all the context it needs to make a decision.

## 3. Safe Execution
I used Python's `ast` module to check the code. This is safer than just running the code, as it lets us verify the logic and syntax without risk.
