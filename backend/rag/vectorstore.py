"""
ChromaDB vector store for job description retrieval.

Persistent storage at backend/rag/data/chroma_db/.
Embeddings are generated externally (via embedder.py) and passed explicitly —
we do not use Chroma's built-in embedding function.

Cosine distance note:
  Chroma returns distances in [0, 2] for cosine space (0 = identical, 2 = opposite).
  We convert to similarity score in [0, 1] as:  similarity = 1 - (distance / 2)
"""
from __future__ import annotations

import os
import chromadb
from chromadb import Collection

from rag import embedder

_CHROMA_DIR = os.path.join(os.path.dirname(__file__), "data", "chroma_db")
_client: chromadb.PersistentClient | None = None


def _get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=_CHROMA_DIR)
    return _client


def get_or_create_collection(name: str = "job_descriptions") -> Collection:
    """Return (or create) the Chroma collection with cosine similarity."""
    return _get_client().get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"},
    )


def upsert_jds(jds: list[dict]) -> None:
    """
    Embed and upsert a list of normalized JD records into Chroma.

    Each record must have: source, source_id, title, company,
    description (already cleaned), tags (list[str]), location, posted_date.

    Chroma metadata values must be scalar, so tags are joined as a comma-separated string.
    """
    collection = get_or_create_collection()

    ids = [f"{jd['source']}:{jd['source_id']}" for jd in jds]
    documents = [jd["description"] for jd in jds]
    metadatas = [
        {
            "title": jd.get("title", ""),
            "company": jd.get("company", ""),
            "source": jd.get("source", ""),
            "tags": ", ".join(jd.get("tags", [])),
            "location": jd.get("location", ""),
            "posted_date": jd.get("posted_date", ""),
        }
        for jd in jds
    ]

    embeddings = embedder.embed_texts(documents)

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )


def retrieve_similar(query: str, k: int = 10) -> list[dict]:
    """
    Retrieve the top-k most similar JDs for a query string.

    Returns list of dicts with keys:
      id, title, company, description, similarity_score (float in [0,1]), metadata
    """
    collection = get_or_create_collection()
    query_embedding = embedder.embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    output = []
    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc_id, doc, meta, dist in zip(ids, documents, metadatas, distances):
        # Chroma cosine distance: 0 = identical, 2 = opposite
        similarity = 1.0 - (dist / 2.0)
        output.append({
            "id": doc_id,
            "title": meta.get("title", ""),
            "company": meta.get("company", ""),
            "description": doc,
            "similarity_score": round(similarity, 4),
            "metadata": meta,
        })

    return output
