from typing import Dict, List


class NLPThreatDetectionService:
    """Keyword and category based threat detection."""

    THREAT_LEXICON = {
        "malware": ["malware", "trojan", "worm", "ransomware", "spyware"],
        "phishing": ["phishing", "credential", "social engineering", "spoofing"],
        "vulnerability": ["cve", "zero-day", "exploit", "vulnerability", "patch"],
        "data-breach": ["data breach", "leak", "exfiltration", "compromised"],
        "ddos": ["ddos", "botnet", "service disruption"],
    }

    def detect(self, text: str) -> Dict[str, List[str] | str]:
        content = text.lower()
        matches: List[str] = []
        category_hits: Dict[str, int] = {}

        for category, keywords in self.THREAT_LEXICON.items():
            for keyword in keywords:
                if keyword in content:
                    matches.append(keyword)
                    category_hits[category] = category_hits.get(category, 0) + 1

        if not matches:
            return {"matched_keywords": [], "category": "unknown"}

        top_category = max(category_hits, key=category_hits.get)
        deduped = sorted(set(matches))
        return {"matched_keywords": deduped, "category": top_category}
