"""
Streamlit UI for the persona-adaptive support agent.

Run with:
    streamlit run app.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import streamlit as st

import config
import persona_detector
import retriever
import response_generator
import escalation
import handoff


st.set_page_config(page_title="Persona-Adaptive Support Agent", page_icon="🎧", layout="wide")

st.title("🎧 Persona-Adaptive Support Agent")
st.caption("RAG-powered support chatbot that adapts its tone to the user and escalates to a human when needed.")

if "history" not in st.session_state:
    st.session_state.history = []  # list of {"user", "assistant"}
if "dissatisfaction_count" not in st.session_state:
    st.session_state.dissatisfaction_count = 0

if not config.GEMINI_API_KEY:
    st.error(
        "GEMINI_API_KEY is not set. Create a `.env` file in the project root "
        "with `GEMINI_API_KEY=your_key_here`, then restart the app."
    )
    st.stop()

if not os.path.exists(config.INDEX_PATH):
    st.error(
        "Vector store not found. Run `python src/ingestion.py` from the project "
        "root first to build the knowledge base index, then restart the app."
    )
    st.stop()

with st.sidebar:
    st.header("Session Info")
    st.metric("Turns so far", len(st.session_state.history))
    st.metric("Dissatisfaction signals", st.session_state.dissatisfaction_count)
    st.divider()
    st.subheader("Escalation settings")
    st.write(f"Confidence threshold: `{config.CONFIDENCE_THRESHOLD}`")
    st.write(f"Dissatisfaction limit: `{config.DISSATISFACTION_LIMIT}`")
    st.divider()
    if st.button("Reset session"):
        st.session_state.history = []
        st.session_state.dissatisfaction_count = 0
        st.rerun()

# Render past turns
for turn in st.session_state.history:
    with st.chat_message("user"):
        st.write(turn["user"])
    with st.chat_message("assistant"):
        st.write(turn["assistant"])
        if turn.get("persona"):
            st.caption(f"Persona: {turn['persona']} · Top score: {turn.get('top_score', 'n/a')}")
        if turn.get("escalated"):
            st.warning(f"⚠️ Escalated to human agent — {turn.get('escalation_reason')}")

query = st.chat_input("Ask a support question...")

if query:
    with st.chat_message("user"):
        st.write(query)

    if escalation.detect_dissatisfaction(query):
        st.session_state.dissatisfaction_count += 1

    with st.chat_message("assistant"):
        with st.spinner("Detecting persona and retrieving context..."):
            persona = persona_detector.detect_persona(query)
            results = retriever.retrieve(query)
            top_score = results[0]["score"] if results else None

        with st.spinner("Generating response..."):
            response_text = response_generator.generate_response(persona, query, results)

        should_escalate, reason = escalation.should_escalate(
            query, top_score, st.session_state.dissatisfaction_count, st.session_state.history
        )

        st.write(response_text)
        st.caption(f"Persona: {persona} · Top retrieval score: {top_score:.3f}" if top_score is not None else f"Persona: {persona}")

        with st.expander("Retrieved sources"):
            for r in results:
                st.write(f"**{r['source']}** (chunk {r['chunk_id']}, score {r['score']:.3f})")
                st.text(r["text"][:300] + ("..." if len(r["text"]) > 300 else ""))

        if should_escalate:
            st.warning(f"⚠️ Escalated to human agent — {reason}")
            summary = handoff.generate_summary(
                persona, query, st.session_state.history, results, reason
            )
            with st.expander("Human handoff summary"):
                st.json(summary)

    st.session_state.history.append({
        "user": query,
        "assistant": response_text,
        "persona": persona,
        "top_score": round(top_score, 3) if top_score is not None else None,
        "escalated": should_escalate,
        "escalation_reason": reason,
    })
