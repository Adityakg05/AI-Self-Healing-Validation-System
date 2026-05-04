"""
LangGraph StateGraph for the AI-Self-Healing-Validation-System.

Defines the agentic workflow with conditional routing and self-correction
loop that allows the agent to iteratively improve fixes based on validation.

Graph Flow:
    START → Investigator → Mechanic → Validator
                ↑                         ↓
                └─────────────────────────┘
                    (if tests fail)       → PR Creator → END
                                              (if tests pass)
"""

from typing import Literal

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from agents import investigator_agent, mechanic_agent, pr_creator_node, validator_node
from config import settings
from state import SREAgentState


def should_continue_investigation(state: SREAgentState) -> Literal["mechanic", "investigator", "end"]:
    """Routing after Investigator Agent."""
    iteration = state.get("iteration_count", 0)
    root_cause_found = state.get("root_cause_identified", False)

    # Prevent infinite loops - safety guard
    if iteration > settings.max_iterations:
        print(f"\n[WARNING] Maximum iterations ({settings.max_iterations}) reached. Ending workflow.")
        return "end"

    # Found it, move forward
    if root_cause_found:
        print("\n[SUCCESS] Root cause identified. Moving to Mechanic Agent...")
        return "mechanic"

    # Keep digging if needed
    print(f"\n[RETRY] Root cause not yet clear. Continuing investigation (attempt {iteration}/3)...)")
    return "investigator"


def should_continue_after_validation(state: SREAgentState) -> Literal["pr_creator", "investigator", "end"]:
    """Routing after Validator Node - self-correction loop."""
    fix_validated = state.get("fix_validated", False)
    iteration = state.get("iteration_count", 0)
    validation_errors = state.get("validation_errors", [])

    # If tests passed, move to PR creation
    if fix_validated:
        print("\n[SUCCESS] Fix validated successfully! Moving to PR creation...")
        return "pr_creator"

    # Safety limit: configurable via MAX_ITERATIONS env var
    if iteration >= settings.max_iterations:
        print(f"\n[ERROR] Maximum attempts ({settings.max_iterations}) reached. Validation still failing.")
        print(f"   Last errors: {validation_errors}")
        print("   Ending workflow without creating PR.")
        return "end"

    # Self-correction
    print("\n[SELF-CORRECTION LOOP] Tests failed. Routing back to Investigator...")
    print(f"   Attempt: {iteration}/3")
    print("   Validation errors will be fed back for reconsideration.")
    return "investigator"


def create_sre_graph() -> StateGraph:
    """Build the LangGraph StateGraph."""
    # Initialize workflow state machine
    workflow = StateGraph(SREAgentState)

    # Register all workflow agents
    workflow.add_node("investigator", investigator_agent)
    workflow.add_node("mechanic", mechanic_agent)
    workflow.add_node("validator", validator_node)
    workflow.add_node("pr_creator", pr_creator_node)

    # Set entry
    workflow.set_entry_point("investigator")

    # Add edges

    # After Investigator
    workflow.add_conditional_edges(
        "investigator",
        should_continue_investigation,
        {
            "mechanic": "mechanic",      # Root cause found → generate fix
            "investigator": "investigator",  # Need more analysis → loop back
            "end": END                    # Max iterations → give up
        }
    )

    # After Mechanic
    workflow.add_edge("mechanic", "validator")

    # After Validator
    # Self-correction loop
    workflow.add_conditional_edges(
        "validator",
        should_continue_after_validation,
        {
            "pr_creator": "pr_creator",      # Tests passed → create PR
            "investigator": "investigator",  # Tests failed → retry with feedback
            "end": END                       # Max attempts → give up
        }
    )

    # After PR Creator
    workflow.add_edge("pr_creator", END)

    # Compile with memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    return app


def visualize_graph(output_file: str = "sre_agent_graph.png"):
    """Generate graph visualization."""
    try:
        from IPython.display import Image
        app = create_sre_graph()

        # Get visualization
        graph_image = app.get_graph().draw_mermaid_png()

        with open(output_file, "wb") as f:
            f.write(graph_image)

        print(f"[SUCCESS] Graph visualization saved to {output_file}")
        return Image(graph_image)
    except ImportError:
        print("[WARNING] Graph visualization requires IPython. Skipping.")
    except Exception as e:
        print(f"[WARNING] Could not generate graph visualization: {e}")


# Create compiled graph
sre_graph = create_sre_graph()


if __name__ == "__main__":
    """Test graph structure."""
    print("Self-Healing SRE Agent Graph")
    print("=" * 60)
    print("\nGraph Structure:")
    print("  START → Investigator")
    print("    ├─ (root cause found) → Mechanic")
    print("    ├─ (need more data)   → Investigator (loop)")
    print("    └─ (max iterations)   → END")
    print("\n  Mechanic → Validator")
    print("\n  Validator")
    print("    ├─ (tests passed)     → PR Creator → END [SUCCESS]")
    print("    ├─ (tests failed)     → Investigator (SELF-CORRECTION LOOP)")
    print("    └─ (max attempts)     → END [FAILED]")
    print("\n" + "=" * 60)
    print("[SUCCESS] Graph definition complete!")
    print("\n[INFO] The self-correction loop allows the agent to:")
    print("   1. Receive test failure feedback from Validator")
    print("   2. Route back to Investigator with error context")
    print("   3. Reconsider the root cause analysis")
    print("   4. Generate an improved fix")
    print("   5. Try again (up to 3 total attempts)")
    print("\nThis makes the agent resilient and able to self-heal!")
