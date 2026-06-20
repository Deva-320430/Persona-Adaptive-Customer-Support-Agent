"""
Shared configuration for the persona-adaptive support agent.

All tunable values live here so they can be changed in one place
instead of hunting through multiple files.
"""
import os
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")
INDEX_PATH = os.path.join(VECTORSTORE_DIR, "index.faiss")
METADATA_PATH = os.path.join(VECTORSTORE_DIR, "metadata.json")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

TOP_K = int(os.getenv("TOP_K", "3"))

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
