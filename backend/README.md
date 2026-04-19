# Backend — AI Resume Analyzer

Flask API with 4 AI endpoints powered by Gemini 2.5 Flash.

## Eval Framework (`evals/`)

The `evals/` directory contains a script-based evaluation framework for the `/api/analyze`
(ATS scoring) endpoint. It calls the AI layer directly — no Flask server required.

### What it measures

| Metric | Description |
|--------|-------------|
| Score-in-range rate | % of test cases where the ATS score fell within expected bounds |
| JSON validity rate | % of responses that parsed as valid Pydantic-validated JSON |
| Avg response time | Mean seconds per Gemini API call |
| Strengths specificity | 0–1 heuristic: do strengths mention numbers, tech names, detail? |
| Contradiction detection | Flags cases where the model praised and criticized the same thing |
| Prompt injection | Checks whether adversarial instructions in the resume text override the prompt |

### Dataset

`evals/datasets/ats_eval_dataset.py` — 15 synthetic test cases:
- 3 strong resumes (expected 75–95)
- 4 medium resumes (expected 50–74)
- 4 weak resumes (expected 20–49)
- 2 edge cases (very short / very long input)
- 2 adversarial cases (prompt injection, irrelevant content)

### How to run

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m evals.run_ats_eval
```

Takes **3–5 minutes** (15 Gemini API calls). Progress is printed case-by-case.

### Output

Results are saved to `evals/results/` (git-ignored):
- `ats_eval_<timestamp>.json` — raw per-case results + aggregate stats
- `ats_eval_<timestamp>.md` — human-readable report with per-case table and failure examples
