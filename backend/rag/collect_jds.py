"""
Run from backend/ with:  python -m rag.collect_jds
"""
import json
import os
import shutil
from collections import Counter
from datetime import datetime, timezone

from rag.scrapers import remoteok_scraper, wwr_scraper

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _dedup(jobs: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for job in jobs:
        key = (job["source"], job["source_id"])
        if key not in seen:
            seen.add(key)
            out.append(job)
    return out


def _print_summary(jobs: list[dict]) -> None:
    by_source = Counter(j["source"] for j in jobs)
    all_tags = [tag for j in jobs for tag in j.get("tags", [])]
    top_tags = Counter(all_tags).most_common(10)
    avg_len = int(sum(len(j["description"]) for j in jobs) / len(jobs)) if jobs else 0

    print(f"\n--- Summary ---")
    print(f"Total jobs:              {len(jobs)}")
    for source, count in sorted(by_source.items()):
        print(f"  {source:<20} {count}")
    print(f"Avg description length:  {avg_len} chars")
    print(f"Top 10 tags:")
    for tag, count in top_tags:
        print(f"  {tag:<30} {count}")


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    # --- RemoteOK ---
    print("Fetching jobs from RemoteOK...")
    try:
        remoteok_jobs = remoteok_scraper.fetch_jobs()
        print(f"  Got {len(remoteok_jobs)} jobs from RemoteOK")
    except RuntimeError as e:
        print(f"  ERROR: {e}")
        remoteok_jobs = []

    # --- We Work Remotely ---
    print("Fetching jobs from We Work Remotely...")
    wwr_jobs = wwr_scraper.fetch_jobs()
    print(f"  Got {len(wwr_jobs)} jobs from WWR")

    # --- Combine and dedup ---
    combined = remoteok_jobs + wwr_jobs
    deduped = _dedup(combined)
    print(
        f"\nFetched {len(remoteok_jobs)} jobs from RemoteOK, "
        f"{len(wwr_jobs)} jobs from WWR, "
        f"{len(deduped)} after dedup"
    )

    if not deduped:
        print("ERROR: No jobs collected. Aborting — do not write empty dataset.")
        return

    # --- Save timestamped file ---
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join(DATA_DIR, f"jds_{timestamp}.json")
    with open(out_path, "w", encoding="utf-8", errors="replace") as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)
    print(f"Saved: {out_path}")

    # --- Save latest.json copy ---
    latest_path = os.path.join(DATA_DIR, "latest.json")
    shutil.copy2(out_path, latest_path)
    print(f"Updated: {latest_path}")

    _print_summary(deduped)


if __name__ == "__main__":
    main()
