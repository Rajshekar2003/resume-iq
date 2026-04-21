import time

from flask import Blueprint, jsonify, request

from prompts.market_synthesis_prompt import MARKET_SYNTHESIS_PROMPT
from prompts.retrieval_query_prompt import RETRIEVAL_QUERY_PROMPT
from rag import vectorstore
from utils.file_handling import FileHandlingError, process_uploaded_resume
from utils.gemini_client import generate_structured_response
from utils.schemas import MarketAnalysisResponse, RetrievalQuery

market_analysis_bp = Blueprint("market_analysis_bp", __name__)

_SIMILARITY_AVG_FLOOR = 0.65
_SIMILARITY_TOP_FLOOR = 0.55
_RETRIEVAL_K = 10


def _format_retrieved_jds(jds: list[dict]) -> str:
    parts = []
    for i, jd in enumerate(jds, 1):
        snippet = jd["description"][:1500]
        parts.append(
            f"JOB {i} [similarity: {jd['similarity_score']:.2f}]\n"
            f"Title: {jd['title']}\n"
            f"Company: {jd['company']}\n"
            f"Description: {snippet}"
        )
    return "\n\n".join(parts)


@market_analysis_bp.route("/api/market-analysis", methods=["POST"])
def market_analysis():
    # Stage 1: Extract resume text
    t0 = time.perf_counter()
    try:
        resume_text = process_uploaded_resume(request)
    except FileHandlingError as e:
        return jsonify({"success": False, "error": str(e)}), e.status_code
    print(f"[market-analysis] Stage 1 (resume extract): {time.perf_counter() - t0:.2f}s")

    try:
        # Stage 2: Generate retrieval query
        t1 = time.perf_counter()
        retrieval_prompt = RETRIEVAL_QUERY_PROMPT.format(resume_text=resume_text)
        retrieval_query: RetrievalQuery = generate_structured_response(
            retrieval_prompt, RetrievalQuery
        )
        print(
            f"[market-analysis] Stage 2 (retrieval query LLM): {time.perf_counter() - t1:.2f}s "
            f"| role='{retrieval_query.role_title}' seniority={retrieval_query.target_seniority}"
        )

        # Stage 3: Build search string
        search_string = f"{retrieval_query.role_title} {' '.join(retrieval_query.key_skills)}"

        # Stage 4: Retrieve similar JDs from ChromaDB
        t2 = time.perf_counter()
        try:
            retrieved = vectorstore.retrieve_similar(search_string, k=_RETRIEVAL_K)
        except Exception as e:
            return jsonify({"success": False, "error": f"Vector store unavailable: {e}"}), 500
        print(f"[market-analysis] Stage 4 (vector retrieval): {time.perf_counter() - t2:.3f}s | got {len(retrieved)} JDs")

        # Stage 5: Relevance floor check
        if not retrieved:
            avg_similarity = 0.0
            top_similarity = 0.0
        else:
            avg_similarity = round(sum(j["similarity_score"] for j in retrieved) / len(retrieved), 4)
            top_similarity = retrieved[0]["similarity_score"]

        floor_triggered = avg_similarity < _SIMILARITY_AVG_FLOOR

        if top_similarity < _SIMILARITY_TOP_FLOOR:
            print(f"[market-analysis] Stage 5: top similarity {top_similarity:.3f} < floor {_SIMILARITY_TOP_FLOOR} — skipping synthesis")
            return jsonify({
                "matched_role_title": retrieval_query.role_title,
                "jobs_analyzed": len(retrieved),
                "top_required_skills": [],
                "candidate_gap_summary": (
                    f"The job database did not return closely matching roles for a '{retrieval_query.role_title}' profile "
                    f"(best match similarity: {top_similarity:.2f}). "
                    "This likely means the scraped corpus doesn't yet cover your specialisation. "
                    "Try running the JD collector again to refresh the dataset, or check the role title detected above."
                ),
                "similarity_floor_triggered": True,
                "avg_similarity_score": avg_similarity,
            })

        # Stage 6: Format retrieved JDs for synthesis prompt
        retrieved_jds_text = _format_retrieved_jds(retrieved)

        # Stage 7: Synthesize market insights
        t3 = time.perf_counter()
        synthesis_prompt = MARKET_SYNTHESIS_PROMPT.format(
            resume_text=resume_text,
            retrieved_jds_text=retrieved_jds_text,
            matched_role_title=retrieval_query.role_title,
        )
        result: MarketAnalysisResponse = generate_structured_response(
            synthesis_prompt, MarketAnalysisResponse
        )
        print(f"[market-analysis] Stage 7 (synthesis LLM): {time.perf_counter() - t3:.2f}s")

        # Stage 8: Override placeholder values with real computed values
        result.matched_role_title = retrieval_query.role_title
        result.jobs_analyzed = len(retrieved)
        result.avg_similarity_score = avg_similarity
        result.similarity_floor_triggered = floor_triggered

        print(f"[market-analysis] Total: {time.perf_counter() - t0:.2f}s")
        return jsonify(result.model_dump())

    except RuntimeError as e:
        return jsonify({"success": False, "error": f"Market analysis failed: {e}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected server error: {e}"}), 500
