"""
Build the ChromaDB index from the scraped JD dataset.

Run from backend/ with:  python -m rag.build_index
"""
import glob
import json
import os
import re
import time

from rag.cleaner import clean_jd_description
from rag import vectorstore

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Tech keywords for auto-tagging WWR jobs (which have no tags from the RSS feed)
_TECH_TERMS = [
    "Python", "JavaScript", "TypeScript", "React", "Vue", "Angular", "Node.js",
    "Node", "Django", "Flask", "FastAPI", "Spring", "Java", "Go", "Golang",
    "Rust", "Ruby", "Rails", "PHP", "Swift", "Kotlin", "C++", "C#", ".NET",
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Terraform", "Ansible",
    "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Kafka", "Elasticsearch",
    "GraphQL", "REST", "gRPC", "CI/CD", "Git", "Linux", "Bash",
    "Machine Learning", "Deep Learning", "NLP", "LLM", "PyTorch", "TensorFlow",
    "Pandas", "NumPy", "Spark", "Airflow", "dbt",
    "React Native", "Flutter", "iOS", "Android",
]

_TECH_PATTERN = re.compile(
    "|".join(re.escape(t) for t in _TECH_TERMS),
    re.IGNORECASE,
)


def _auto_tag(description: str) -> list[str]:
    """Extract tech keywords present in the description (case-insensitive)."""
    found = set()
    for match in _TECH_PATTERN.finditer(description):
        # Normalize to the canonical casing from _TECH_TERMS
        found.add(match.group(0).lower())
    # Return up to 8 tags, sorted for determinism
    return sorted(found)[:8]


def _load_jds() -> tuple[list[dict], str]:
    latest = os.path.join(DATA_DIR, "latest.json")
    if os.path.exists(latest):
        path = latest
    else:
        candidates = sorted(glob.glob(os.path.join(DATA_DIR, "jds_*.json")))
        if not candidates:
            raise FileNotFoundError(
                f"No JD data found in {DATA_DIR}. Run python -m rag.collect_jds first."
            )
        path = candidates[-1]

    with open(path, encoding="utf-8") as f:
        return json.load(f), path


def main() -> None:
    jds, path = _load_jds()
    print(f"Loading {len(jds)} JDs from {path}")

    # Clean descriptions and auto-tag any records missing tags
    for jd in jds:
        jd["description"] = clean_jd_description(jd["description"])
        if not jd.get("tags"):
            jd["tags"] = _auto_tag(jd["description"])

    # Embed and upsert in one shot (sentence-transformers batches internally)
    print(f"Embedding {len(jds)} job descriptions...")
    start = time.time()
    vectorstore.upsert_jds(jds)
    elapsed = time.time() - start
    print(f"Done. Embedded and stored {len(jds)} JDs in {elapsed:.1f}s")

    # Stats
    collection = vectorstore.get_or_create_collection()
    count = collection.count()
    chroma_dir = os.path.join(DATA_DIR, "chroma_db")
    disk_bytes = sum(
        os.path.getsize(os.path.join(dp, f))
        for dp, _, files in os.walk(chroma_dir)
        for f in files
    )
    disk_mb = disk_bytes / (1024 * 1024)
    print(f"Collection '{collection.name}': {count} documents, {disk_mb:.1f} MB on disk")


if __name__ == "__main__":
    main()
