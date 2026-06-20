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
    "provided context — never invent facts, numbers, or policies that aren't "
    "in it. But you SHOULD synthesize and explain what the context does say, "
    "even if it doesn't phrase the answer exactly the way the user asked. "
    "Only say you lack information if the context is truly silent on the "
    "topic, not just because it doesn't state a specific number or outcome."
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
- Use only facts, numbers, and policies present in the context above — never invent them.
- If the context discusses the topic at all (even indirectly, e.g. policies, frameworks,
  or related procedures), explain what it says rather than refusing. A relevant policy
  or process IS a valid answer, even if it doesn't give a single concrete number.
- Only respond with "I don't have enough information to answer that — let me connect
  you with someone who can help." if the context is genuinely unrelated to the question.
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
