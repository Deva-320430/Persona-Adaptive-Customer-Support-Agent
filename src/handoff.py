"""
Handoff summary: builds a structured summary for a human agent when
a conversation is escalated, using real conversation history rather
than empty stub fields.
"""
from datetime import datetime, timezone


def generate_summary(persona, query, history, retrieved_sources, escalation_reason):
    """
    persona: detected persona string
    query: the triggering user message
    history: list of {"user": ..., "assistant": ...} turns so far (not including current)
    retrieved_sources: list of {"source": ..., "score": ...} from retrieval
    escalation_reason: string explanation from escalation.should_escalate
    """
    attempted_steps = []
    for turn in history:
        attempted_steps.append(f"Agent suggested: {turn['assistant'][:200]}")

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "persona": persona,
        "triggering_message": query,
        "escalation_reason": escalation_reason,
        "conversation_history": history,
        "attempted_steps": attempted_steps,
        "documents_referenced": [
            {"source": s["source"], "relevance_score": round(s["score"], 3)}
            for s in retrieved_sources
        ],
        "recommendation": (
            "Human review required. See escalation_reason and attempted_steps "
            "above before responding to avoid repeating unsuccessful suggestions."
        ),
    }


def format_summary_for_display(summary):
    """Pretty-prints a summary dict as readable text (used by the CLI)."""
    lines = []
    lines.append("=" * 60)
    lines.append("HUMAN HANDOFF SUMMARY")
    lines.append("=" * 60)
    lines.append(f"Timestamp:        {summary['timestamp']}")
    lines.append(f"Persona:          {summary['persona']}")
    lines.append(f"Reason:           {summary['escalation_reason']}")
    lines.append(f"Triggering msg:   {summary['triggering_message']}")
    lines.append("")
    lines.append("Documents referenced:")
    for doc in summary["documents_referenced"]:
        lines.append(f"  - {doc['source']} (score: {doc['relevance_score']})")
    lines.append("")
    if summary["attempted_steps"]:
        lines.append("Steps already attempted by the bot:")
        for step in summary["attempted_steps"]:
            lines.append(f"  - {step}")
    else:
        lines.append("No prior bot responses in this conversation.")
    lines.append("")
    lines.append(f"Recommendation: {summary['recommendation']}")
    lines.append("=" * 60)
    return "\n".join(lines)
