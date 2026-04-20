"""
We Work Remotely scraper — parses the RSS feed for the programming jobs category.
The URL returns application/rss+xml directly (no HTML page scraping needed).
"""
import html
import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import requests

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

FEED_URL = "https://weworkremotely.com/categories/remote-programming-jobs"
HEADERS = {"User-Agent": "ResumeAnalyzer-EducationalScraper/1.0"}
MIN_DESCRIPTION_LENGTH = 300
MAX_JOBS = 50

TITLE_KEYWORDS = {
    "engineer", "developer", "software", "backend", "frontend",
    "fullstack", "full-stack", "ml", "ai", "data", "devops",
    "sre", "python", "javascript", "react", "node",
}


def _is_relevant(title: str) -> bool:
    title_lower = title.lower()
    return any(kw in title_lower for kw in TITLE_KEYWORDS)


def _strip_html(raw: str) -> str:
    decoded = html.unescape(raw)
    return BeautifulSoup(decoded, "html.parser").get_text(separator=" ").strip()


def _source_id_from_link(link: str) -> str:
    return link.rstrip("/").split("/")[-1].split("?")[0] if link else ""


def fetch_jobs() -> list[dict]:
    """Fetch and normalize tech jobs from the WWR RSS feed."""
    try:
        resp = requests.get(FEED_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[WWR] WARNING: Could not reach RSS feed: {e}")
        return []

    # Parse as XML via lxml (already installed) for reliability
    try:
        soup = BeautifulSoup(resp.content, features="xml")
    except Exception:
        # lxml XML parser unavailable — fall back to html.parser
        soup = BeautifulSoup(resp.text, "html.parser")

    items = soup.find_all("item")
    if not items:
        print("[WWR] WARNING: No <item> elements found in feed — structure may have changed")
        return []

    results = []
    for item in items:
        raw_title = item.find("title")
        raw_desc = item.find("description")
        raw_link = item.find("link")
        raw_region = item.find("region")
        raw_pubdate = item.find("pubDate")

        if not raw_title or not raw_desc:
            continue

        # RSS title format is usually "Company: Job Title"
        full_title = raw_title.get_text(strip=True)
        if ": " in full_title:
            company, title = full_title.split(": ", 1)
        else:
            company, title = "", full_title

        if not _is_relevant(title) and not _is_relevant(full_title):
            continue

        description = _strip_html(raw_desc.get_text())
        if len(description) < MIN_DESCRIPTION_LENGTH:
            continue

        link = raw_link.get_text(strip=True) if raw_link else ""
        source_id = _source_id_from_link(link)
        location = raw_region.get_text(strip=True) if raw_region else "Remote"
        posted_date = raw_pubdate.get_text(strip=True) if raw_pubdate else ""

        results.append({
            "source": "wwr",
            "source_id": source_id,
            "title": title,
            "company": company,
            "description": description,
            "tags": [],  # WWR RSS doesn't include tags — Day 9 can infer them
            "location": location,
            "posted_date": posted_date,
        })

        if len(results) >= MAX_JOBS:
            break

    return results
