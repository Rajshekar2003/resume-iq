import time
import requests
from bs4 import BeautifulSoup

API_URL = "https://remoteok.com/api"
HEADERS = {"User-Agent": "ResumeAnalyzer-EducationalScraper/1.0"}

TITLE_KEYWORDS = {
    "engineer", "developer", "software", "backend", "frontend",
    "fullstack", "full-stack", "ml", "ai", "data", "devops",
    "sre", "python", "javascript", "react", "node",
}

MIN_DESCRIPTION_LENGTH = 300


def _strip_html(html: str) -> str:
    if not html:
        return ""
    return BeautifulSoup(html, "html.parser").get_text(separator=" ").strip()


def _is_relevant(title: str) -> bool:
    title_lower = title.lower()
    return any(kw in title_lower for kw in TITLE_KEYWORDS)


def fetch_jobs() -> list[dict]:
    """Fetch and normalize tech jobs from the RemoteOK public JSON API."""
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"RemoteOK API unreachable: {e}") from e

    raw = response.json()
    # First element is a legal notice dict, not a job — skip it
    jobs_raw = [item for item in raw if isinstance(item, dict) and "id" in item and "position" in item]

    results = []
    for job in jobs_raw:
        title = job.get("position", "")
        if not _is_relevant(title):
            continue

        description = _strip_html(job.get("description", ""))
        if len(description) < MIN_DESCRIPTION_LENGTH:
            continue

        tags = job.get("tags", [])
        if isinstance(tags, list):
            tags = [str(t) for t in tags]
        else:
            tags = []

        results.append({
            "source": "remoteok",
            "source_id": str(job.get("id", "")),
            "title": title,
            "company": job.get("company", ""),
            "description": description,
            "tags": tags,
            "location": job.get("location", "Worldwide"),
            "posted_date": job.get("date", ""),
        })

    return results
