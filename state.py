"""State management for AI-Self-Healing-Validation-System.

Defines TypedDict structure used as state for LangGraph StateGraph. The state flows through all agent nodes and tracks the workflow.
"""

from operator import add
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage


class SREAgentState(TypedDict):
    """State schema for Self-Healing SRE Agent workflow.

    Phases:
    1. Investigation: Fetch and analyze logs
    2. Fix Generation: Create code to fix issue
    3. Validation: Verify fix is valid Python
    4. PR Creation: Open GitHub Pull Request

    Attributes:
        messages: Conversation history between agents and LLM

        error_logs: Raw application logs

        root_cause_identified: Boolean flag if root cause found

        root_cause_analysis: Explanation of what caused the error

        fix_code: Generated Python code that fixes the issue

        fix_validated: Boolean flag if fix is valid

        validation_errors: List of syntax or validation errors

        pr_status: Status of PR creation: "pending", "created", "failed"

        pr_url: URL of created GitHub Pull Request

        iteration_count: Counter to prevent infinite loops

        error_timestamp: Timestamp when error was detected
    """

    # Message history
    messages: Annotated[Sequence[BaseMessage], add]

    # Logs fetched during investigation phase
    error_logs: str
    root_cause_identified: bool
    root_cause_analysis: str

    # Fix generation
    fix_code: str
    fix_validated: bool
    validation_errors: list[str]

    # PR creation
    pr_status: str  # "pending", "created", "failed"
    pr_url: str

    # Control flow
    iteration_count: int
    error_timestamp: str


def create_initial_state(error_message: str) -> dict:
    """Create initial state for new SRE workflow."""
    from datetime import datetime, timezone

    from langchain_core.messages import HumanMessage

    return {
        "messages": [HumanMessage(content=error_message)],
        "error_logs": "",
        "root_cause_identified": False,
        "root_cause_analysis": "",
        "fix_code": "",
        "fix_validated": False,
        "validation_errors": [],
        "pr_status": "pending",
        "pr_url": "",
        "iteration_count": 0,
        "error_timestamp": datetime.now(timezone.utc).isoformat(),
    }
