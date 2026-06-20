"""
Retrieval layer: loads the prebuilt FAISS index + metadata and
exposes a single retrieve() function used by the chatbot.

Uses the Gemini embedding API (via llm_client.embed_text) for the
query vector, matching whatever embedded the documents in ingestion.py.
"""
import json
import os

import faiss
import numpy as np

import config
import llm_client

_index = None
_metadata = None


def _ensure_loaded():
    global _index, _metadata

    if _index is None or _metadata is None:
        if not os.path.exists(config.INDEX_PATH) or not os.path.exists(config.METADATA_PATH):
            raise FileNotFoundError(
                "Vector store not found. Run `python src/ingestion.py` first to build it."
            )
        _index = faiss.read_index(config.INDEX_PATH)
        with open(config.METADATA_PATH, "r", encoding="utf-8") as f:
            _metadata = json.load(f)


def retrieve(query, top_k=None):
    """
    Returns a list of dicts:
        {"text": ..., "source": ..., "chunk_id": ..., "score": float}
    score is cosine similarity in roughly [-1, 1], HIGHER is better.
    """
    _ensure_loaded()
    top_k = top_k or config.TOP_K

    query_embedding = llm_client.embed_text(query, task_type="RETRIEVAL_QUERY")
    query_vec = np.array([query_embedding], dtype=np.float32)
    faiss.normalize_L2(query_vec)

    scores, indices = _index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        chunk = _metadata[idx]
        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "score": float(score),
        })
    return results


if __name__ == "__main__":
    # quick manual smoke test
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "How do I reset my password?"
    for r in retrieve(q):
        print(f"[{r['score']:.3f}] {r['source']} (chunk {r['chunk_id']})")
        print(r["text"][:150].replace("\n", " "), "...\n")
