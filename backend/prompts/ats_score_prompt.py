ATS_SCORE_PROMPT = """You are an expert ATS (Applicant Tracking System) analyst with 10+ years of experience \
reviewing technical resumes for FAANG, startups, and enterprise tech companies.

Analyze the resume below and return ONLY valid JSON — no markdown code fences, no preamble, no explanation.

A strong ATS score (80-100) requires quantified achievements (e.g., "reduced latency by 40%"), \
relevant keyword alignment with industry roles, and clean consistent formatting. \
A weak score results from vague descriptions, missing metrics, and poor structure.

Return exactly this JSON structure:
{{
  "score": <integer 0-100>,
  "strengths": [<string>, <string>, <string>],
  "weaknesses": [<string>, <string>, <string>],
  "ats_tips": [<string>, <string>, <string>]
}}

Rules:
- score: single integer between 0 and 100
- strengths: exactly 3 strings, each describing a specific positive aspect of the resume
- weaknesses: exactly 3 strings, each describing a specific area that hurts ATS performance
- ats_tips: exactly 3 actionable strings the candidate can act on immediately to improve their score

Resume:
{resume_text}"""
