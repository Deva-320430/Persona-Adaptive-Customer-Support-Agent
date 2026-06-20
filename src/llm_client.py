"""
Thin wrapper around the Gemini API so the rest of the codebase
doesn't need to know SDK details, and so we have one place to
handle missing keys / errors gracefully.
"""
from google import genai
from google.genai import types

import config

_client = None


def get_client():
    global _client
    if _client is None:
        if not config.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to a .env file "
                "in the project root: GEMINI_API_KEY=your_key_here"
            )
        _client = genai.Client(api_key=config.GEMINI_API_KEY)
    return _client


def generate(prompt, system_instruction=None, temperature=0.3, model=None):
    """Single-turn text generation. Returns the response text (stripped)."""
    client = get_client()
    model = model or config.GEMINI_MODEL

    gen_config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=gen_config,
    )

    text = getattr(response, "text", None)
    if not text:
        # Defensive: surface something rather than crash on an empty/blocked response
        return ""
    return text.strip()


def embed_texts(texts, task_type="RETRIEVAL_DOCUMENT", batch_size=20):
    """
    Embeds a list of strings using the Gemini embedding API.

    task_type: "RETRIEVAL_DOCUMENT" when embedding knowledge-base chunks,
               "RETRIEVAL_QUERY" when embedding a user's question.
               Using the matching type improves retrieval quality.
    batch_size: number of texts per API call. Kept conservative since
               gemini-embedding-001 has been reported to hit rate limits
               on the free tier with large batches.

    Returns a list of float lists (one embedding vector per input text,
    same order as the input).
    """
    client = get_client()
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.models.embed_content(
            model=config.EMBEDDING_MODEL,
            contents=batch,
            config=types.EmbedContentConfig(task_type=task_type),
        )
        for item in response.embeddings:
            all_embeddings.append(list(item.values))

    return all_embeddings


def embed_text(text, task_type="RETRIEVAL_QUERY"):
    """Convenience wrapper for embedding a single string (e.g. a user query)."""
    return embed_texts([text], task_type=task_type)[0]
