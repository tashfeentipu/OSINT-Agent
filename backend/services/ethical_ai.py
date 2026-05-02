import re
from typing import Dict


class EthicalAIService:
    """Applies privacy-aware redaction and transparency metadata."""

    LOCATION_TERMS = {
        "london", "paris", "new york", "tokyo", "berlin", "madrid", "rome",
        "united states", "uk", "england", "india", "china", "russia",
    }

    def sanitize_text(self, text: str) -> Dict[str, str]:
        cleaned = text
        cleaned = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[redacted-email]", cleaned)
        cleaned = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[redacted-ip]", cleaned)
        cleaned = re.sub(r"\b([A-Z][a-z]+\s[A-Z][a-z]+)\b", "[redacted-name]", cleaned)

        for location in self.LOCATION_TERMS:
            pattern = re.compile(rf"\b{re.escape(location)}\b", re.IGNORECASE)
            cleaned = pattern.sub("[redacted-location]", cleaned)

        return {
            "sanitized_text": cleaned,
            "transparency_note": "Sensitive entities such as possible names, emails, IPs, and known locations are redacted heuristically.",
        }
