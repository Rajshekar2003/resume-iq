"""
Pure metric functions for evaluating ATS score responses.

All functions take primitive inputs and return primitive outputs — no API calls, no side effects.
"""

import json
import re


def check_score_in_range(actual_score: int, expected_range: tuple[int, int]) -> bool:
    """Return True if actual_score falls within [min, max] inclusive."""
    lo, hi = expected_range
    return lo <= actual_score <= hi


def check_no_contradiction(strengths: list[str], weaknesses: list[str]) -> bool:
    """
    Return False if any noun phrase appears in both strengths and weaknesses.

    Heuristic: extract 2-3 word noun-like phrases (lowercased) from each list,
    then check for overlap. A hit in both lists suggests the model praised and
    criticised the same thing, which is a contradiction.
    """
    def extract_noun_phrases(sentences: list[str]) -> set[str]:
        phrases: set[str] = set()
        for sentence in sentences:
            words = re.findall(r"[a-zA-Z]+", sentence.lower())
            # bigrams and trigrams as candidate noun phrases
            for i in range(len(words)):
                if i + 1 < len(words):
                    phrases.add(f"{words[i]} {words[i+1]}")
                if i + 2 < len(words):
                    phrases.add(f"{words[i]} {words[i+1]} {words[i+2]}")
        return phrases

    # Skip very short inputs that don't produce meaningful phrases
    if not strengths or not weaknesses:
        return True

    strength_phrases = extract_noun_phrases(strengths)
    weakness_phrases = extract_noun_phrases(weaknesses)

    overlap = strength_phrases & weakness_phrases

    # Filter out stop-word-only bigrams that produce false positives
    stopwords = {
        "of the", "in the", "to the", "and the", "is a", "the resume",
        "the candidate", "a strong", "a good", "a lack", "the use",
        "of a", "with a", "for the", "in a", "on the", "that the",
    }
    meaningful_overlap = overlap - stopwords

    return len(meaningful_overlap) == 0


def check_strengths_specificity(strengths: list[str]) -> float:
    """
    Return a 0.0–1.0 specificity score averaged across all strength strings.

    Per-strength heuristics (each is a boolean → 0 or 1):
      1. Contains a number or percentage (quantification signal)
      2. Contains a recognisable technology name (specificity signal)
      3. Longer than 50 characters (detail signal)

    The score for each strength is the mean of those three booleans.
    The overall score is the mean across all strengths.
    """
    if not strengths:
        return 0.0

    tech_pattern = re.compile(
        r"\b(python|java|typescript|javascript|go|rust|c\+\+|react|angular|vue|"
        r"node|django|flask|fastapi|spring|kubernetes|docker|aws|gcp|azure|"
        r"redis|postgres|postgresql|mysql|mongodb|kafka|terraform|airflow|"
        r"spark|pandas|pytorch|tensorflow|scikit|sklearn|sql|git|ci/cd|"
        r"graphql|rest|api|microservice|devops|mlops|agile|scrum)\b",
        re.IGNORECASE,
    )
    number_pattern = re.compile(r"\d+\.?\d*\s*(%|percent|x\b|ms\b|s\b|k\b|m\b|\$)?")

    per_strength_scores: list[float] = []
    for s in strengths:
        has_number = bool(number_pattern.search(s))
        has_tech = bool(tech_pattern.search(s))
        is_detailed = len(s) > 50
        per_strength_scores.append((has_number + has_tech + is_detailed) / 3.0)

    return sum(per_strength_scores) / len(per_strength_scores)


def check_response_time_acceptable(elapsed_seconds: float, threshold: float = 15.0) -> bool:
    """Return True if the API call completed within the threshold (default 15 s)."""
    return elapsed_seconds <= threshold


def check_json_valid(raw_response: str) -> bool:
    """
    Return True if raw_response is parseable JSON.

    Used when calling the model directly (outside the Pydantic layer) to verify
    that the raw output is well-formed before schema validation.
    """
    try:
        json.loads(raw_response)
        return True
    except (json.JSONDecodeError, TypeError):
        return False
