import re

# Lines starting with these labels are WWR RSS artifacts — not job content
_ARTIFACT_PREFIXES = re.compile(
    r"^\s*(headquarters|url|website|apply|how to apply|application url"
    r"|apply here|apply now|apply at|apply link)\s*:",
    re.IGNORECASE | re.MULTILINE,
)

_MULTI_WHITESPACE = re.compile(r"\n{3,}")
_MULTI_SPACE = re.compile(r" {2,}")


def clean_jd_description(text: str) -> str:
    """Remove WWR RSS artifacts and normalize whitespace."""
    lines = text.splitlines()
    cleaned_lines = [ln for ln in lines if not _ARTIFACT_PREFIXES.match(ln)]
    result = "\n".join(cleaned_lines)
    result = _MULTI_WHITESPACE.sub("\n\n", result)
    result = _MULTI_SPACE.sub(" ", result)
    return result.strip()
