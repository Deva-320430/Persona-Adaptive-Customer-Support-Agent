"""
Response generation: takes the detected persona, the user query, and
retrieved context chunks, and produces a persona-adapted answer that
is grounded only in the provided context.
"""
import config
import llm_client

STYLE_GUIDES = {
    "Technical Expert": (
        "Be precise and technical. Include root cause where relevant, "
        "specific error conditions, and concrete troubleshooting steps. "
        "Don't over-explain basics they likely already know."
    ),
    "Frustrated User": (
        "Be warm, empathetic, and reassuring. Acknowledge the frustration "
        "briefly without being patronizing. Use simple, plain language and "
        "short steps. Avoid jargon."
    ),
    "Business Executive": (
        "Be concise and lead with business impact (scope, timeline, risk). "
        "Avoid technical deep-dives unless asked. If relevant, mention SLA "
        "or escalation timelines."
    ),
}

SYSTEM_INSTRUCTION = (
    "You are a customer support assistant. You must answer using ONLY the "
    "provided context. If the context does not contain enough information "
    "to answer, say so plainly — do not guess or invent details."
)

PROMPT_TEMPLATE = """Persona: {persona}
Response style for this persona: {style}

Context (retrieved knowledge base excerpts):
\"\"\"
{context}
\"\"\"

User question:
\"\"\"{query}\"\"\"

Rules:
- Use only the information in the context above.
- If the context does not contain the answer, respond with exactly:
  "I don't have enough information to answer that — let me connect you with someone who can help."
- Do not fabricate steps, policies, or numbers not present in the context.
- Match the response style described above.
"""


def generate_response(persona, query, context_chunks):
    """
    context_chunks: list of retrieved chunk dicts (from retriever.retrieve)
    Returns the generated answer text.
    """
    style = STYLE_GUIDES.get(persona, STYLE_GUIDES["Frustrated User"])

    if context_chunks:
        context_text = "\n\n---\n\n".join(c["text"] for c in context_chunks)
    else:
        context_text = "(no relevant context retrieved)"

    prompt = PROMPT_TEMPLATE.format(
        persona=persona,
        style=style,
        context=context_text,
        query=query,
    )

    return llm_client.generate(prompt, system_instruction=SYSTEM_INSTRUCTION, temperature=0.3)
