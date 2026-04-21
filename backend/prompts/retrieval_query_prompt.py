RETRIEVAL_QUERY_PROMPT = """You are an expert technical recruiter who converts candidate resumes into \
precise job-search queries for semantic vector retrieval.

Read the resume carefully, then extract the information needed to find the most relevant job descriptions \
in a vector database of remote tech roles.

Return ONLY valid JSON — no markdown code fences, no preamble, no explanation.

Your task:
1. Identify the single best-fit role title for this candidate (role_title). \
Be specific: "Senior Python Backend Engineer" beats "Software Engineer". \
Use common job-board terminology so the query matches real listings.
2. Extract the 3-10 most important technical skills for retrieval (key_skills). \
These are the terms that, if present in a job description, would make it relevant to this candidate. \
Prioritize: primary languages, core frameworks/tools, and domain keywords (e.g. "distributed systems", "ML inference"). \
Exclude soft skills and generic terms like "teamwork" or "agile".
3. Assess the candidate's seniority level (target_seniority): \
"junior" (0-2 years), "mid" (2-5 years), "senior" (5-10 years), "staff_plus" (10+ years or staff/principal titles).

Return exactly this JSON structure:
{{
  "role_title": "<specific job title string>",
  "key_skills": ["<skill 1>", "<skill 2>", ...],
  "target_seniority": "<junior|mid|senior|staff_plus>"
}}

Resume:
{resume_text}"""