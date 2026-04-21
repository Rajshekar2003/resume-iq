"""
Manual retrieval quality test — run from backend/ with:
    python -m rag.test_retrieval
"""
from rag import vectorstore

QUERIES = [
    "Senior Python Backend Developer with AWS experience",
    "React frontend engineer",
    "Machine learning engineer with production deployment experience",
    "DevOps engineer Kubernetes Terraform",
    "Full stack JavaScript developer Node.js React",
]

SNIPPET_LEN = 200
TOP_K = 3


def main() -> None:
    print("=" * 70)
    print("RAG RETRIEVAL TEST")
    print("=" * 70)

    for query in QUERIES:
        print(f"\nQUERY: {query}")
        print("-" * 60)
        results = vectorstore.retrieve_similar(query, k=TOP_K)
        if not results:
            print("  (no results — is the index built?)")
            continue
        for i, r in enumerate(results, 1):
            snippet = r["description"].replace("\n", " ")[:SNIPPET_LEN]
            print(f"  [{i}] score={r['similarity_score']:.4f}  |  {r['title']} @ {r['company']}")
            print(f"       {snippet}...")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
