"""
ATS scoring evaluation runner.

Run from backend/:
    python -m evals.run_ats_eval

Makes one Gemini API call per test case (~15 calls total). Expect 3-5 minutes runtime.
Results are saved to evals/results/ as JSON + Markdown.
"""

import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure backend/ is on the path when executed as __main__
_backend_dir = Path(__file__).resolve().parent.parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

from evals.datasets.ats_eval_dataset import ATS_EVAL_DATASET, EvalCase
from evals.metrics import (
    check_json_valid,
    check_no_contradiction,
    check_response_time_acceptable,
    check_score_in_range,
    check_strengths_specificity,
)
from prompts.ats_score_prompt import ATS_SCORE_PROMPT
from utils.gemini_client import generate_structured_response
from utils.schemas import AtsScoreResponse

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def _prompt_hash(prompt_template: str) -> str:
    """MD5 first 8 chars of the prompt template — used as a version fingerprint."""
    return hashlib.md5(prompt_template.encode()).hexdigest()[:8]


def run_single_case(case: EvalCase) -> dict:
    """Run one eval case; return a result dict regardless of success or failure."""
    prompt = ATS_SCORE_PROMPT.format(resume_text=case["resume_text"])

    result: dict = {
        "id": case["id"],
        "description": case["description"],
        "expected_score_range": list(case["expected_score_range"]),
        "success": False,
        "exception": None,
        "score": None,
        "elapsed_seconds": None,
        "score_in_range": False,
        "response_time_ok": False,
        "no_contradiction": False,
        "strengths_specificity": 0.0,
        "json_valid": False,
        "raw_response_sample": None,
    }

    t_start = time.monotonic()
    try:
        response: AtsScoreResponse = generate_structured_response(prompt, AtsScoreResponse)
        elapsed = time.monotonic() - t_start

        result["success"] = True
        result["elapsed_seconds"] = round(elapsed, 2)
        result["score"] = response.score
        result["json_valid"] = True  # Pydantic validation passed → JSON was valid
        result["score_in_range"] = check_score_in_range(response.score, case["expected_score_range"])
        result["response_time_ok"] = check_response_time_acceptable(elapsed)
        result["no_contradiction"] = check_no_contradiction(response.strengths, response.weaknesses)
        result["strengths_specificity"] = round(check_strengths_specificity(response.strengths), 3)
        result["raw_response_sample"] = {
            "strengths": response.strengths,
            "weaknesses": response.weaknesses,
            "ats_tips": response.ats_tips,
        }

    except Exception as exc:
        elapsed = time.monotonic() - t_start
        result["elapsed_seconds"] = round(elapsed, 2)
        result["exception"] = str(exc)

    return result


def compute_aggregate(results: list[dict]) -> dict:
    total = len(results)
    successful = [r for r in results if r["success"]]
    n_ok = len(successful)

    adversarial_ids = {"ats_014", "ats_015"}
    adversarial_results = [r for r in results if r["id"] in adversarial_ids]
    injection_case = next((r for r in results if r["id"] == "ats_014"), None)
    injection_bypassed = (
        injection_case is not None
        and injection_case["success"]
        and injection_case["score"] == 100
    )

    return {
        "total_cases": total,
        "successful_cases": n_ok,
        "json_validity_rate": round(n_ok / total, 3) if total else 0.0,
        "score_in_range_count": sum(1 for r in successful if r["score_in_range"]),
        "score_in_range_rate": round(
            sum(1 for r in successful if r["score_in_range"]) / n_ok, 3
        ) if n_ok else 0.0,
        "avg_response_time_seconds": round(
            sum(r["elapsed_seconds"] for r in successful) / n_ok, 2
        ) if n_ok else 0.0,
        "avg_strengths_specificity": round(
            sum(r["strengths_specificity"] for r in successful) / n_ok, 3
        ) if n_ok else 0.0,
        "contradictions_detected": sum(
            1 for r in successful if not r["no_contradiction"]
        ),
        "response_time_violations": sum(
            1 for r in successful if not r["response_time_ok"]
        ),
        "prompt_injection_bypassed": injection_bypassed,
        "adversarial_scores": {
            r["id"]: r["score"] for r in adversarial_results if r["success"]
        },
    }


def build_markdown_report(
    results: list[dict], aggregate: dict, prompt_hash: str, timestamp: str
) -> str:
    lines: list[str] = []

    lines.append(f"# ATS Eval Report — {timestamp}")
    lines.append("")
    lines.append(f"**Prompt version (MD5 prefix):** `{prompt_hash}`")
    lines.append("")

    # Summary table
    lines.append("## Aggregate Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    agg = aggregate
    lines.append(f"| Total cases | {agg['total_cases']} |")
    lines.append(f"| Successful (no exception) | {agg['successful_cases']} |")
    lines.append(f"| JSON validity rate | {agg['json_validity_rate']:.1%} |")
    lines.append(
        f"| Score-in-range | {agg['score_in_range_count']}/{agg['successful_cases']} "
        f"({agg['score_in_range_rate']:.1%}) |"
    )
    lines.append(f"| Avg response time | {agg['avg_response_time_seconds']} s |")
    lines.append(f"| Avg strengths specificity | {agg['avg_strengths_specificity']:.3f} |")
    lines.append(f"| Contradictions detected | {agg['contradictions_detected']} |")
    lines.append(f"| Response time violations (>15s) | {agg['response_time_violations']} |")
    lines.append(f"| Prompt injection bypassed | {'YES ⚠️' if agg['prompt_injection_bypassed'] else 'No ✓'} |")
    lines.append("")

    # Adversarial scores
    lines.append("### Adversarial Case Scores")
    lines.append("")
    for case_id, score in agg["adversarial_scores"].items():
        label = "Prompt injection" if case_id == "ats_014" else "Irrelevant content"
        flag = " ⚠️ (injection worked!)" if case_id == "ats_014" and score == 100 else ""
        lines.append(f"- **{case_id}** ({label}): score = **{score}**{flag}")
    lines.append("")

    # Per-case results table
    lines.append("## Per-Case Results")
    lines.append("")
    lines.append("| ID | Description | Expected | Actual | In Range | Specificity | Time (s) | OK |")
    lines.append("|----|-------------|----------|--------|----------|-------------|----------|----|")
    for r in results:
        expected = f"{r['expected_score_range'][0]}–{r['expected_score_range'][1]}"
        actual = str(r["score"]) if r["score"] is not None else "ERR"
        in_range = "✓" if r["score_in_range"] else "✗"
        specificity = f"{r['strengths_specificity']:.2f}" if r["success"] else "—"
        time_s = f"{r['elapsed_seconds']:.1f}" if r["elapsed_seconds"] is not None else "—"
        ok = "✓" if r["success"] else "✗"
        desc_short = r["description"][:55] + "…" if len(r["description"]) > 55 else r["description"]
        lines.append(
            f"| {r['id']} | {desc_short} | {expected} | {actual} | {in_range} | {specificity} | {time_s} | {ok} |"
        )
    lines.append("")

    # Failures
    failures = [r for r in results if r["success"] and not r["score_in_range"]]
    exceptions = [r for r in results if not r["success"]]

    if failures:
        lines.append("## Out-of-Range Cases")
        lines.append("")
        for r in failures:
            lines.append(f"### {r['id']} — {r['description']}")
            lines.append(f"- Expected: {r['expected_score_range'][0]}–{r['expected_score_range'][1]}")
            lines.append(f"- Actual score: **{r['score']}**")
            if r["raw_response_sample"]:
                lines.append(f"- Strengths: {r['raw_response_sample']['strengths']}")
                lines.append(f"- Weaknesses: {r['raw_response_sample']['weaknesses']}")
            lines.append("")

    if exceptions:
        lines.append("## Exceptions / Errors")
        lines.append("")
        for r in exceptions:
            lines.append(f"### {r['id']}")
            lines.append(f"- Error: `{r['exception']}`")
            lines.append("")

    return "\n".join(lines)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    prompt_hash = _prompt_hash(ATS_SCORE_PROMPT)

    print(f"\n{'='*60}")
    print(f"  ATS Eval Runner")
    print(f"  Cases: {len(ATS_EVAL_DATASET)} | Prompt hash: {prompt_hash}")
    print(f"  Estimated time: 3-5 minutes (15 Gemini API calls)")
    print(f"{'='*60}\n")

    results: list[dict] = []
    total = len(ATS_EVAL_DATASET)

    for i, case in enumerate(ATS_EVAL_DATASET, start=1):
        print(f"  [{i:02d}/{total}] {case['id']} — {case['description'][:60]}...")
        result = run_single_case(case)
        results.append(result)

        status = "✓" if result["success"] else "✗ ERROR"
        score_str = f"score={result['score']}" if result["score"] is not None else result["exception"]
        range_str = f" {'IN' if result['score_in_range'] else 'OUT OF'} range" if result["success"] else ""
        print(f"         {status} {score_str}{range_str} ({result['elapsed_seconds']}s)\n")

    aggregate = compute_aggregate(results)

    # Save JSON
    json_path = RESULTS_DIR / f"ats_eval_{timestamp}.json"
    payload = {
        "timestamp": timestamp,
        "prompt_hash": prompt_hash,
        "aggregate": aggregate,
        "results": results,
    }
    json_path.write_text(json.dumps(payload, indent=2))

    # Save Markdown
    md_path = RESULTS_DIR / f"ats_eval_{timestamp}.md"
    md_content = build_markdown_report(results, aggregate, prompt_hash, timestamp)
    md_path.write_text(md_content)

    # Console summary
    agg = aggregate
    print(f"\n{'='*60}")
    print(f"  RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"  Cases run:          {agg['total_cases']}")
    print(f"  Successful:         {agg['successful_cases']}/{agg['total_cases']}")
    print(f"  Score in range:     {agg['score_in_range_count']}/{agg['successful_cases']} ({agg['score_in_range_rate']:.1%})")
    print(f"  Avg response time:  {agg['avg_response_time_seconds']}s")
    print(f"  Avg specificity:    {agg['avg_strengths_specificity']:.3f}")
    print(f"  Contradictions:     {agg['contradictions_detected']}")
    print(f"  Injection bypass:   {'YES ⚠️' if agg['prompt_injection_bypassed'] else 'No ✓'}")
    print(f"\n  JSON  → {json_path}")
    print(f"  MD    → {md_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
