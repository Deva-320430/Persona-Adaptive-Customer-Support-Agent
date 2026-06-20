"""
CLI entry point for the persona-adaptive support agent.

Usage:
    python src/chatbot.py

Type 'exit' or 'quit' to end the session.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
import persona_detector
import retriever
import response_generator
import escalation
import handoff


def run_cli():
    print("=" * 60)
    print("Persona-Adaptive Support Agent (CLI)")
    print("Type 'exit' or 'quit' to end the session.")
    print("=" * 60)

    history = []
    dissatisfaction_count = 0

    while True:
        try:
            query = input("\nUser: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            break

        if not query:
            continue
        if query.lower() in ("exit", "quit"):
            print("Session ended.")
            break

        if escalation.detect_dissatisfaction(query):
            dissatisfaction_count += 1

        try:
            persona = persona_detector.detect_persona(query)
        except RuntimeError as e:
            print(f"\n[Config error] {e}")
            break

        results = retriever.retrieve(query)
        top_score = results[0]["score"] if results else None

        context_text_for_log = ", ".join(r["source"] for r in results) if results else "none"

        response_text = response_generator.generate_response(persona, query, results)

        should_escalate, reason = escalation.should_escalate(
            query, top_score, dissatisfaction_count, history
        )

        print(f"\n[Persona detected: {persona}]")
        print(f"[Sources retrieved: {context_text_for_log}]")
        if top_score is not None:
            print(f"[Top retrieval confidence: {top_score:.3f}]")
        print(f"\nAssistant: {response_text}")

        if should_escalate:
            summary = handoff.generate_summary(
                persona, query, history, results, reason
            )
            print("\n" + handoff.format_summary_for_display(summary))

        history.append({"user": query, "assistant": response_text})


if __name__ == "__main__":
    run_cli()
