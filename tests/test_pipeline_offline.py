"""
Offline smoke test for the pipeline wiring.

This does NOT call the real Gemini API or download embedding models —
it monkeypatches llm_client.generate() and retriever.retrieve() so we
can verify persona_detector -> response_generator -> escalation ->
handoff are wired together correctly before you ever spend an API
call or wait on a model download.

Run with:
    python tests/test_pipeline_offline.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

import llm_client
import retriever
import persona_detector
import response_generator
import escalation
import handoff


def fake_generate(prompt, system_instruction=None, temperature=0.3, model=None):
    """Pretend-LLM: returns canned answers based on the user's actual message,
    extracted from between the triple-quoted message markers in the prompt,
    rather than the whole prompt (which always contains persona-description
    boilerplate text like "APIs" regardless of what the user actually said)."""
    is_classification = system_instruction is not None and "persona" in system_instruction.lower()

    if is_classification:
        parts = prompt.split('"""')
        user_message = parts[1] if len(parts) >= 2 else prompt
        msg_lower = user_message.lower()

        if "401" in msg_lower or "logs" in msg_lower or "root cause" in msg_lower:
            return "Technical Expert"
        if "impact" in msg_lower or "operations" in msg_lower or "business" in msg_lower:
            return "Business Executive"
        return "Frustrated User"

    return "Here is a mocked grounded answer based on the retrieved context."


def fake_retrieve(query, top_k=None):
    query_lower = query.lower()
    if "sap ariba" in query_lower or "custom middleware" in query_lower:
        # Simulate a poor match -> should trigger escalation on low confidence
        return [{"text": "irrelevant chunk", "source": "deployment_guide.md", "chunk_id": 0, "score": 0.10}]
    return [
        {"text": "Relevant mocked chunk 1", "source": "password_reset.md", "chunk_id": 0, "score": 0.81},
        {"text": "Relevant mocked chunk 2", "source": "password_reset.md", "chunk_id": 1, "score": 0.62},
    ]


def run_case(label, query, dissatisfaction_count=0, history=None):
    history = history or []
    persona = persona_detector.detect_persona(query)
    results = retriever.retrieve(query)
    top_score = results[0]["score"] if results else None
    response_text = response_generator.generate_response(persona, query, results)
    should_escalate, reason = escalation.should_escalate(query, top_score, dissatisfaction_count, history)

    print(f"--- {label} ---")
    print(f"Query:        {query}")
    print(f"Persona:      {persona}")
    print(f"Top score:    {top_score}")
    print(f"Response:     {response_text}")
    print(f"Escalate?:    {should_escalate} ({reason})")

    if should_escalate:
        summary = handoff.generate_summary(persona, query, history, results, reason)
        assert summary["persona"] == persona
        assert summary["escalation_reason"] == reason
        assert isinstance(summary["attempted_steps"], list)
        print("Handoff summary generated OK.")
    print()


def main():
    llm_client.generate = fake_generate
    retriever.retrieve = fake_retrieve

    print("=" * 60)
    print("OFFLINE PIPELINE SMOKE TEST (mocked LLM + retriever)")
    print("=" * 60 + "\n")

    run_case("Technical Expert, normal confidence", "API authentication keeps failing with 401 errors, can you check the logs?")
    run_case("Business Executive, normal confidence", "How will this outage impact our operations?")
    run_case(
        "Frustrated User, repeated dissatisfaction -> escalate",
        "This still doesn't work, I've tried everything already",
        dissatisfaction_count=2,
    )
    run_case(
        "Low confidence retrieval -> escalate",
        "Can your platform integrate with SAP Ariba using custom middleware?",
    )
    run_case(
        "Escalation keyword -> escalate",
        "I want to file a chargeback for last month's billing issue",
    )

    print("=" * 60)
    print("ALL SMOKE TEST CASES RAN WITHOUT ERROR.")
    print("=" * 60)


if __name__ == "__main__":
    main()
