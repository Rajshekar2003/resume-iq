"""
Local sentence embedding using all-MiniLM-L6-v2.

Model: all-MiniLM-L6-v2
- Output dimension: 384
- Runs entirely on CPU — no GPU required
- ~80 MB download, cached to ~/.cache/huggingface after first use
- ~30-60 seconds to load on first call; subsequent calls are fast
- Optimized for semantic similarity / retrieval tasks
"""
from __future__ import annotations
import os
import warnings

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
warnings.filterwarnings("ignore", message=".*unauthenticated requests.*")

_model = None


def _get_model():
    global _model
    if _model is None:
        print("Loading embedding model (first time only, ~30-60s)...")
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Embedding model ready.")
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embed a list of strings into 384-dimensional vectors.

    sentence-transformers handles batching automatically.
    Returns a list of float lists (not numpy arrays) for JSON-serializability.
    """
    model = _get_model()
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings.tolist()
