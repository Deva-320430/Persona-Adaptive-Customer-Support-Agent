"""
Shared configuration for the persona-adaptive support agent.

All tunable values live here so they can be changed in one place
instead of hunting through multiple files.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Gemini settings ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Stable, free-tier-friendly default. Swap to "gemini-3.5-flash" or
# "gemini-3.1-flash-lite" if you want a newer/cheaper model later —
# this is the only line you need to change.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

# --- Embedding settings ---
# Uses the Gemini embedding API directly (confirmed available on your key)
# instead of a local Hugging Face model — no separate model download needed,
# everything runs through the same API key.
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")
INDEX_PATH = os.path.join(VECTORSTORE_DIR, "index.faiss")
METADATA_PATH = os.path.join(VECTORSTORE_DIR, "metadata.json")

# --- Chunking ---
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

# --- Retrieval ---
TOP_K = int(os.getenv("TOP_K", "3"))

# --- Escalation ---
# We use cosine similarity (via normalized embeddings), where HIGHER
# is better and the range is roughly [-1, 1]. This is the opposite
# direction from raw FAISS L2 distance, so don't reuse this threshold
# if you switch index types without checking the metric.
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.35"))
DISSATISFACTION_LIMIT = int(os.getenv("DISSATISFACTION_LIMIT", "2"))

ESCALATION_KEYWORDS = [
    "billing dispute",
    "legal",
    "lawsuit",
    "chargeback",
    "refund",
    "account hacked",
    "compromised",
    "data loss",
    "sue",
]

DISSATISFACTION_PHRASES = [
    "this doesn't work",
    "still not working",
    "not helpful",
    "useless",
    "frustrated",
    "annoyed",
    "tried everything",
    "already tried",
    "speak to a human",
    "speak to a person",
    "real person",
]

PERSONAS = ["Technical Expert", "Frustrated User", "Business Executive"]
