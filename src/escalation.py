"""
Escalation logic: decides whether a query should be handed off to a
human agent.

IMPORTANT: our retriever returns cosine similarity (via normalized
embeddings + inner-product FAISS index), where HIGHER scores mean a
BETTER match. So low confidence == escalate, which is the opposite
direction from raw FAISS L2 distance. If you ever swap index types,
re-check this logic against retriever.py's docstring.
"""
import config


def should_escalate(query, top_score, dissatisfaction_count, history=None):
    """
    Returns (should_escalate: bool, reason: str | None)

    top_score: best similarity score from retrieval (higher = better match)
    dissatisfaction_count: number of dissatisfaction signals seen so far in the conversation
    history: optional list of past turns, used to detect repeated low-confidence answers
    """
    query_lower = query.lower()

    
    matched_keywords = [k for k in config.ESCALATION_KEYWORDS if k in query_lower]
    if matched_keywords:
        return True, f"Escalation keyword(s) detected: {', '.join(matched_keywords)}"

    
    if top_score is not None and top_score < config.CONFIDENCE_THRESHOLD:
        return True, f"Low retrieval confidence (score={top_score:.3f} < threshold={config.CONFIDENCE_THRESHOLD})"

    
    if dissatisfaction_count >= config.DISSATISFACTION_LIMIT:
        return True, f"Dissatisfaction signals reached limit ({dissatisfaction_count} >= {config.DISSATISFACTION_LIMIT})"

    return False, None


def detect_dissatisfaction(message):
    """Returns True if the message contains a dissatisfaction signal phrase."""
    message_lower = message.lower()
    return any(phrase in message_lower for phrase in config.DISSATISFACTION_PHRASES)
